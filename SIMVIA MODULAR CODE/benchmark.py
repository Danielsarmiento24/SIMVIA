import cv2
import time
import json
import os
import psutil
from ultralytics import YOLO

MODELOS = [
    "yolov8n_ncnn_model",
    "yolov8s_ncnn_model",
    "yolov9t_ncnn_model",
    "yolov10n_ncnn_model",
    "yolo11n_ncnn_model",
    "yolo26n_ncnn_model"
]

VEHICULOS = {0: 'auto', 1: 'bus', 2: 'camion', 3: 'moto'}
FRAMES_PRUEBA = 100
RESULTADOS_FILE = "benchmark_resultados.json"

def obtener_tam_modelo(nombre):
    ruta = os.path.join(os.path.expanduser("~"), ".config/Ultralytics", nombre)
    if not os.path.exists(ruta):
        ruta = nombre
    if os.path.exists(ruta):
        return round(os.path.getsize(ruta) / (1024 * 1024), 1)
    return 0

def benchmark_modelo(nombre_modelo, cap):
    print(f"\n{'='*50}")
    print(f"Probando: {nombre_modelo}")
    print(f"{'='*50}")

    try:
        print("  Descargando/cargando modelo...")
        model = YOLO(nombre_modelo)
        print("  Modelo cargado. Iniciando prueba...")
    except Exception as e:
        print(f"  ERROR cargando modelo: {e}")
        return None

    tiempos = []
    confianzas = []
    detecciones_vehiculo = 0
    ram_inicio = psutil.Process().memory_info().rss / (1024 * 1024)

    # Warmup
    for _ in range(5):
        ret, frame = cap.read()
        if ret:
            frame_small = cv2.resize(frame, (320, 240))
            model(frame_small, verbose=False, imgsz=320)

    # Benchmark real
    frames_ok = 0
    for i in range(FRAMES_PRUEBA):
        ret, frame = cap.read()
        if not ret:
            continue

        frame_small = cv2.resize(frame, (320, 240))
        t_inicio = time.time()
        results = model(frame_small, conf=0.4, verbose=False, imgsz=320)
        t_fin = time.time()

        tiempos.append((t_fin - t_inicio) * 1000)
        frames_ok += 1

        for box in results[0].boxes:
            clase_id = int(box.cls[0])
            confianzas.append(float(box.conf[0]))
            if clase_id in VEHICULOS:
                detecciones_vehiculo += 1

        if (i + 1) % 20 == 0:
            fps_actual = 1000 / (sum(tiempos[-20:]) / 20)
            print(f"  Progreso: {i+1}/{FRAMES_PRUEBA} frames | FPS: {fps_actual:.1f}")

    ram_fin = psutil.Process().memory_info().rss / (1024 * 1024)

    if not tiempos:
        return None

    tiempo_prom = sum(tiempos) / len(tiempos)
    fps_prom = 1000 / tiempo_prom
    confianza_prom = sum(confianzas) / len(confianzas) if confianzas else 0
    tam_modelo = obtener_tam_modelo(nombre_modelo)

    resultado = {
        "modelo": nombre_modelo.replace(".pt", ""),
        "fps_promedio": round(fps_prom, 1),
        "tiempo_inferencia_ms": round(tiempo_prom, 1),
        "tiempo_min_ms": round(min(tiempos), 1),
        "tiempo_max_ms": round(max(tiempos), 1),
        "confianza_promedio": round(confianza_prom * 100, 1),
        "detecciones_vehiculo": detecciones_vehiculo,
        "ram_uso_mb": round(ram_fin - ram_inicio, 1),
        "tam_modelo_mb": tam_modelo,
        "frames_analizados": frames_ok
    }

    print(f"\n  RESULTADO {nombre_modelo}:")
    print(f"  FPS promedio:        {resultado['fps_promedio']}")
    print(f"  Inferencia promedio: {resultado['tiempo_inferencia_ms']} ms")
    print(f"  Confianza promedio:  {resultado['confianza_promedio']}%")
    print(f"  RAM adicional:       {resultado['ram_uso_mb']} MB")

    del model
    return resultado

def main():
    print("Iniciando benchmark de modelos YOLO en Raspberry Pi 5")
    print(f"Frames por modelo: {FRAMES_PRUEBA}")
    print(f"Modelos a evaluar: {len(MODELOS)}")

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("ERROR: No se pudo abrir la camara")
        return

    resultados = []
    for modelo in MODELOS:
        resultado = benchmark_modelo(modelo, cap)
        if resultado:
            resultados.append(resultado)
            # Guardar progreso
            with open(RESULTADOS_FILE, 'w') as f:
                json.dump(resultados, f, indent=2)
            print(f"  Resultado guardado en {RESULTADOS_FILE}")

    cap.release()

    print(f"\n{'='*50}")
    print("BENCHMARK COMPLETADO")
    print(f"{'='*50}")
    print(f"\nRanking por FPS:")
    ranking = sorted(resultados, key=lambda x: x['fps_promedio'], reverse=True)
    for i, r in enumerate(ranking, 1):
        print(f"  {i}. {r['modelo']}: {r['fps_promedio']} FPS | {r['tiempo_inferencia_ms']}ms | {r['confianza_promedio']}% confianza")

    print(f"\nResultados guardados en: {RESULTADOS_FILE}")

if __name__ == "__main__":
    main()
