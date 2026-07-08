#!/usr/bin/env python3
"""
calibrar.py - Calibracion del sistema de flujo vehicular con video pregrabado.
Usa los mismos parametros y modelo que servidor.py para comparar
conteo automatico vs conteo manual.
"""

import cv2
from ultralytics import YOLO
import time
import json
import os
import sys
import argparse
from datetime import datetime
from collections import defaultdict

# Mismos parametros que servidor.py
DISTANCIA_REAL_METROS = 8.0
LINEA_A_Y = 237
LINEA_B_Y = 337
LINEA_X_MIN = 0
CONFIANZA_MIN = 0.5
CONFIANZA_MIN_MOTO = 0.25
VEHICULOS = {0: "auto", 1: "bus", 2: "camion", 3: "moto"}
MODELO_DEFAULT = "yolo26n_ncnn_model"


def main():
    parser = argparse.ArgumentParser(description="Calibracion con video pregrabado")
    parser.add_argument("video", help="Ruta al archivo de video")
    parser.add_argument("--modelo", default=MODELO_DEFAULT)
    parser.add_argument("--guardar", action="store_true", help="Guardar video anotado")
    parser.add_argument("--confianza", type=float, default=CONFIANZA_MIN)
    parser.add_argument("--confianza-moto", type=float, default=CONFIANZA_MIN_MOTO, dest="confianza_moto")
    parser.add_argument("--linea-a", type=int, default=LINEA_A_Y, dest="linea_a")
    parser.add_argument("--linea-b", type=int, default=LINEA_B_Y, dest="linea_b")
    parser.add_argument("--linea-x-min", type=int, default=LINEA_X_MIN, dest="linea_x_min")
    parser.add_argument("--distancia", type=float, default=DISTANCIA_REAL_METROS)
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: No se encuentra {args.video}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"CALIBRACION  -  {os.path.basename(args.video)}")
    print(f"{'='*60}")
    print(f"Modelo:     {args.modelo}")
    print(f"Linea A:    y={args.linea_a}px  (referencia 640x480)")
    print(f"Linea B:    y={args.linea_b}px  (referencia 640x480)")
    print(f"X minimo:   x={args.linea_x_min}px  (referencia 640x480)")
    print(f"Distancia:  {args.distancia} m entre lineas")
    print(f"Confianza:  {args.confianza} (motos: {args.confianza_moto})")

    print("\nCargando modelo...")
    model = YOLO(args.modelo)

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        print(f"ERROR: No se pudo abrir {args.video}")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_video = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duracion = total_frames / fps_video

    print(f"Video:      {w}x{h} @ {fps_video:.1f}fps | {duracion:.1f}s | {total_frames} frames\n")

    # Escalar lineas A/B de la referencia 640x480 a la resolucion real del video
    escala_y = h / 480.0
    escala_x = w / 640.0
    linea_a_px = int(args.linea_a * escala_y)
    linea_b_px = int(args.linea_b * escala_y)
    linea_x_min_px = int(args.linea_x_min * escala_x)

    print(f"Lineas escaladas a {w}x{h}:  A=y{linea_a_px}px  B=y{linea_b_px}px  X_min=x{linea_x_min_px}px\n")

    writer = None
    if args.guardar:
        out_path = args.video.rsplit(".", 1)[0] + "_calibrado.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps_video, (w, h))
        print(f"Guardando video anotado en: {out_path}\n")

    registro = {}
    conteo = defaultdict(int)
    ids_contados = set()
    velocidades = []
    frame_count = 0
    t_inicio = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Inferencia a 320x240 igual que servidor.py
        frame_small = cv2.resize(frame, (320, 240))
        results = model.track(
            frame_small,
            conf=min(args.confianza, args.confianza_moto),
            verbose=False,
            imgsz=320,
            tracker="bytetrack.yaml",
            persist=True,
        )

        boxes = results[0].boxes if results[0].boxes is not None else []

        for box in boxes:
            if box.id is None:
                continue
            clase_id = int(box.cls[0])
            if clase_id not in VEHICULOS:
                continue
            confianza = float(box.conf[0])
            umbral = args.confianza_moto if clase_id == 3 else args.confianza
            if confianza < umbral:
                continue

            vehicle_id = int(box.id[0])
            tipo = VEHICULOS[clase_id]

            # Escalar coordenadas de 320x240 a resolucion real
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1 = int(x1 * escala_x * 2)
            x2 = int(x2 * escala_x * 2)
            y1 = int(y1 * escala_y * 2)
            y2 = int(y2 * escala_y * 2)
            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2

            if vehicle_id not in registro:
                registro[vehicle_id] = {"tipo": tipo, "frame_A": None, "velocidad": None}

            # Cruce linea A
            if (centro_x >= linea_x_min_px and linea_a_px <= centro_y < linea_b_px
                    and registro[vehicle_id]["frame_A"] is None):
                registro[vehicle_id]["frame_A"] = frame_count

            # Cruce linea B -> conteo y velocidad
            if (
                centro_x >= linea_x_min_px
                and centro_y >= linea_b_px
                and registro[vehicle_id]["frame_A"] is not None
                and registro[vehicle_id]["velocidad"] is None
                and vehicle_id not in ids_contados
            ):
                frames_entre = frame_count - registro[vehicle_id]["frame_A"]
                tiempo = frames_entre / fps_video
                if tiempo > 0:
                    vel = (args.distancia / tiempo) * 3.6
                    if 3 <= vel <= 120:  # rango realista de velocidad
                        registro[vehicle_id]["velocidad"] = vel
                        velocidades.append(vel)
                        conteo[tipo] += 1
                        ids_contados.add(vehicle_id)
                        total_ahora = sum(conteo.values())
                        print(
                            f"  [frame {frame_count:5d}/{total_frames}] "
                            f"{tipo:6s} ID:{vehicle_id:3d} "
                            f"-> {vel:.1f} km/h  |  Total acumulado: {total_ahora}"
                        )

            # Dibujar
            contado = vehicle_id in ids_contados
            color = (0, 200, 50) if contado else (0, 180, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            vel_txt = (
                f"{registro[vehicle_id]['velocidad']:.1f}km/h"
                if registro[vehicle_id]["velocidad"]
                else "..."
            )
            cv2.putText(
                frame, f"{tipo} {vel_txt}",
                (x1, max(y1 - 8, 12)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2,
            )
            cv2.putText(
                frame, f"ID:{vehicle_id}",
                (x1, min(y2 + 18, h - 4)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 230, 0), 1,
            )

        # Lineas de referencia
        cv2.line(frame, (0, linea_a_px), (w, linea_a_px), (255, 50, 50), 2)
        cv2.putText(frame, f"Linea A (ref y={args.linea_a})",
                    (8, linea_a_px - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 50, 50), 2)
        cv2.line(frame, (0, linea_b_px), (w, linea_b_px), (50, 50, 255), 2)
        cv2.putText(frame, f"Linea B (ref y={args.linea_b})",
                    (8, linea_b_px - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (50, 50, 255), 2)
        if linea_x_min_px > 0:
            cv2.line(frame, (linea_x_min_px, 0), (linea_x_min_px, h), (50, 230, 230), 2)
            cv2.putText(frame, f"X min (ref x={args.linea_x_min})",
                        (linea_x_min_px + 6, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (50, 230, 230), 2)

        # HUD
        total_ahora = sum(conteo.values())
        cv2.putText(frame, f"Detectados: {total_ahora}",
                    (8, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 220), 2)
        progreso = frame_count / total_frames * 100
        cv2.putText(frame, f"{progreso:.0f}%",
                    (w - 70, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 180, 180), 2)

        if writer:
            writer.write(frame)

        if frame_count % 150 == 0:
            elapsed = time.time() - t_inicio
            fps_proc = frame_count / elapsed
            restante = (total_frames - frame_count) / fps_proc if fps_proc > 0 else 0
            print(
                f"  Progreso: {frame_count}/{total_frames} ({progreso:.0f}%) "
                f"| {fps_proc:.1f} fps proc | ~{restante:.0f}s restantes"
            )

    cap.release()
    if writer:
        writer.release()

    # Reporte final
    elapsed = time.time() - t_inicio
    total_vehiculos = sum(conteo.values())
    flujo_veh_h = round((total_vehiculos / duracion) * 3600) if duracion > 0 else 0
    vel_prom = sum(velocidades) / len(velocidades) if velocidades else 0
    vel_max = max(velocidades) if velocidades else 0
    vel_min = min(velocidades) if velocidades else 0

    print(f"\n{'='*60}")
    print("RESULTADO DE CALIBRACION")
    print(f"{'='*60}")
    print(f"Duracion video:    {duracion:.1f}s")
    print(f"Tiempo proceso:    {elapsed:.1f}s  ({elapsed/duracion:.1f}x tiempo real)")
    print(f"\nCONTEO AUTOMATICO:")
    print(f"  Total:    {total_vehiculos}")
    for tipo, n in sorted(conteo.items()):
        print(f"  {tipo:8s}: {n}")
    print(f"\nFLUJO ESTIMADO:    {flujo_veh_h} veh/h")
    print(f"\nVELOCIDADES:")
    print(f"  Promedio: {vel_prom:.1f} km/h")
    print(f"  Maxima:   {vel_max:.1f} km/h")
    print(f"  Minima:   {vel_min:.1f} km/h")

    reporte = {
        "archivo": os.path.basename(args.video),
        "fecha_ejecucion": datetime.now().isoformat(),
        "parametros": {
            "modelo": args.modelo,
            "linea_a_y_ref": args.linea_a,
            "linea_b_y_ref": args.linea_b,
            "linea_a_y_real": linea_a_px,
            "linea_b_y_real": linea_b_px,
            "linea_x_min_ref": args.linea_x_min,
            "linea_x_min_real": linea_x_min_px,
            "distancia_m": args.distancia,
            "confianza_min": args.confianza,
        },
        "video": {
            "resolucion": f"{w}x{h}",
            "fps": round(fps_video, 2),
            "duracion_s": round(duracion, 1),
            "total_frames": total_frames,
        },
        "resultado_automatico": {
            "total_vehiculos": total_vehiculos,
            "conteo_por_tipo": dict(conteo),
            "flujo_veh_h": flujo_veh_h,
            "velocidad_promedio_kmh": round(vel_prom, 1),
            "velocidad_maxima_kmh": round(vel_max, 1),
            "velocidad_minima_kmh": round(vel_min, 1),
        },
        "conteo_manual": None,
        "precision_pct": None,
        "notas": "",
    }

    reporte_path = args.video.rsplit(".", 1)[0] + "_calibracion.json"
    with open(reporte_path, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"\nReporte JSON: {reporte_path}")
    print(f"{'='*60}")
    print("\n>>> Siguiente paso:")
    print("    Cuenta los vehiculos manualmente en el video y")
    print(f"    escribe el total en 'conteo_manual' del reporte JSON.")
    print("    La precision se calcula como: automatico/manual * 100\n")


if __name__ == "__main__":
    main()
