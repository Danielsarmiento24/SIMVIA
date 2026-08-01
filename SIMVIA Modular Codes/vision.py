import asyncio
import queue
import threading
import time
from datetime import datetime

import cv2
from ultralytics import YOLO

import config
import estado
from comunicacion import enviar_datos

stream_activo = False
frame_anotado = None
frame_raw_ultimo = None
frame_lock = threading.Lock()
frame_raw_lock = threading.Lock()
stream_event = threading.Event()
stream_cal_event = threading.Event()
frame_queue = queue.Queue(maxsize=config.QUEUE_SIZE)
modo_calibracion = threading.Event()
reset_pendiente = threading.Event()


def generar_frames():
    global stream_activo
    stream_activo = True
    ultimo = 0.0
    while stream_activo:
        if not stream_event.wait(timeout=0.2):
            continue
        stream_event.clear()
        ahora = time.time()
        if ahora - ultimo < 0.067:
            continue
        ultimo = ahora
        with frame_lock:
            if frame_anotado is None:
                continue
            frame_stream = cv2.resize(frame_anotado, (480, 360))
            ret, buffer = cv2.imencode(".jpg", frame_stream, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


def generar_frames_calibracion():
    ultimo = 0.0
    while True:
        if not stream_cal_event.wait(timeout=0.5):
            continue
        stream_cal_event.clear()
        ahora = time.time()
        if ahora - ultimo < 0.033:
            continue
        ultimo = ahora
        with frame_raw_lock:
            if frame_raw_ultimo is None:
                continue
            frame = frame_raw_ultimo.copy()
        ret, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        if not ret:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")


def hilo_captura():
    global frame_raw_ultimo
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    print("Hilo de captura iniciado...")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        with frame_raw_lock:
            frame_raw_ultimo = frame.copy()
        stream_cal_event.set()
        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
        frame_queue.put(frame)
    cap.release()


def hilo_inferencia(loop_asyncio):
    global frame_anotado
    model = YOLO("yolo26n_cacique_ncnn_model")
    registro = {}
    fps_counter = 0
    fps_start = time.time()
    fps_actual = 0
    print("Hilo de inferencia iniciado con YOLO26n NCNN...")
    while True:
        if reset_pendiente.is_set():
            registro.clear()
            reset_pendiente.clear()
        if modo_calibracion.is_set():
            time.sleep(0.1)
            continue

        try:
            frame = frame_queue.get(timeout=1)
        except queue.Empty:
            continue

        with config.config_lock:
            linea_a = config.LINEA_A_Y
            linea_b = config.LINEA_B_Y
            dist_m = config.DISTANCIA_REAL_METROS
            x_min = config.LINEA_X_MIN

        frame_small = cv2.resize(frame, (320, 240))
        results = model.track(frame_small, conf=config.CONFIANZA_MIN_MOTO,
                              verbose=False, imgsz=320,
                              tracker="bytetrack.yaml", persist=True)
        for box in results[0].boxes:
            if box.id is None:
                continue
            clase_id = int(box.cls[0])
            if clase_id not in config.VEHICULOS:
                continue
            confianza = float(box.conf[0])
            umbral = config.CONFIANZA_MIN_MOTO if clase_id == 3 else config.CONFIANZA_MIN
            if confianza < umbral:
                continue
            vehicle_id = int(box.id[0])
            tipo = config.VEHICULOS[clase_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1, x2 = x1 * 2, x2 * 2
            y1, y2 = y1 * 2, y2 * 2
            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2
            if vehicle_id not in registro:
                registro[vehicle_id] = {"tipo": tipo, "tiempo_A": None, "velocidad": None}
            if (centro_x >= x_min and linea_a <= centro_y < linea_b
                    and registro[vehicle_id]["tiempo_A"] is None):
                registro[vehicle_id]["tiempo_A"] = time.time()
            if (centro_x >= x_min and centro_y >= linea_b and registro[vehicle_id]["tiempo_A"] is not None
                    and registro[vehicle_id]["velocidad"] is None):
                tiempo = time.time() - registro[vehicle_id]["tiempo_A"]
                if tiempo > 0:
                    velocidad = round((dist_m / tiempo) * 3.6, 1)
                    if 3 <= velocidad <= 120:  # rango realista de velocidad
                        registro[vehicle_id]["velocidad"] = velocidad
                        with estado.timestamps_lock:
                            estado.timestamps_cruces.append(time.time())
                        with estado.velocidades_lock:
                            estado.velocidades_ventana.append((time.time(), velocidad))
                        with estado.conteo_lock:
                            if vehicle_id not in estado.ids_contados:
                                estado.ids_contados.add(vehicle_id)
                                estado.conteo[tipo] = estado.conteo.get(tipo, 0) + 1
                        flujo, vehiculos_5min = estado.calcular_flujo()
                        datos = {
                            "id": vehicle_id, "tipo": tipo, "velocidad_kmh": velocidad,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "conteo": dict(estado.conteo), "flujo_veh_h": flujo,
                            "vehiculos_5min": vehiculos_5min
                        }
                        print(f"Vehiculo {vehicle_id} | {tipo} | {velocidad} km/h | Flujo: {flujo} veh/h")
                        asyncio.run_coroutine_threadsafe(enviar_datos(datos), loop_asyncio)
            velocidad_txt = (f"{registro[vehicle_id]['velocidad']:.1f} km/h"
                             if registro[vehicle_id]["velocidad"] else "...")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{tipo} {velocidad_txt}",
                        (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{vehicle_id}",
                        (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
        ids_en_frame = {int(b.id[0]) for b in results[0].boxes if b.id is not None}
        for vid in list(registro.keys()):
            if vid not in ids_en_frame:
                del registro[vid]

        cv2.line(frame, (0, linea_a), (640, linea_a), (255, 0, 0), 2)
        cv2.putText(frame, "Linea A", (10, linea_a - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.line(frame, (0, linea_b), (640, linea_b), (0, 0, 255), 2)
        cv2.putText(frame, "Linea B", (10, linea_b - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if x_min > 0:
            cv2.line(frame, (x_min, 0), (x_min, 480), (0, 255, 255), 2)
            cv2.putText(frame, "X min", (x_min + 5, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        fps_counter += 1
        if time.time() - fps_start >= 1.0:
            fps_actual = fps_counter
            fps_counter = 0
            fps_start = time.time()
            asyncio.run_coroutine_threadsafe(
                enviar_datos({"tipo": "fps", "fps": fps_actual}), loop_asyncio
            )
        cv2.putText(frame, f"FPS: {fps_actual}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        with frame_lock:
            frame_anotado = frame.copy()
        stream_event.set()
