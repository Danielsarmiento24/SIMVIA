import asyncio
import csv
import json
import os
import time
from datetime import datetime

import requests

import config
import estado

clientes = []

if not os.path.exists(config.LOG_FILE):
    with open(config.LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["timestamp", "flujo_veh_h", "vehiculos_5min"])


async def enviar_datos(datos):
    mensaje = json.dumps(datos)
    desconectados = []
    for cliente in clientes:
        try:
            await cliente.send_text(mensaje)
        except Exception:
            desconectados.append(cliente)
    for c in desconectados:
        clientes.remove(c)


def enviar_a_sheets(datos):
    if not config.SHEETS_URL:
        return
    try:
        requests.post(config.SHEETS_URL, json=datos, timeout=10)
    except Exception as e:
        print(f"Error enviando a Sheets: {e}")


def hilo_log_flujo(loop_asyncio, fan_controller, dht_sensor):
    ultimo_log = time.time()
    ultimo_sensor = time.time()
    while True:
        time.sleep(1)
        ahora = time.time()
        if ahora - ultimo_sensor >= 5:
            ultimo_sensor = ahora
            if fan_controller:
                datos_s = {"tipo": "sensores", **fan_controller.datos()}
                if dht_sensor:
                    datos_s.update(dht_sensor.datos())
                asyncio.run_coroutine_threadsafe(enviar_datos(datos_s), loop_asyncio)
        if ahora - ultimo_log >= config.INTERVALO_LOG_SEG:
            flujo, vehiculos_5min = estado.calcular_flujo()
            ultimo_log = ahora
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(config.LOG_FILE, "a", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow([ts, flujo, vehiculos_5min])
            print(f"Flujo: {flujo} veh/h ({vehiculos_5min} veh en 5 min)")
            estado.guardar_estado()
            with estado.conteo_lock:
                conteo_snap = dict(estado.conteo)
            enviar_a_sheets({
                "timestamp": ts,
                "flujo_veh_h": flujo,
                "vehiculos_5min": vehiculos_5min,
                "autos": conteo_snap.get("auto", 0),
                "motos": conteo_snap.get("moto", 0),
                "buses": conteo_snap.get("bus", 0),
                "camiones": conteo_snap.get("camion", 0),
                "vel_prom": estado.calcular_vel_prom()
            })
            asyncio.run_coroutine_threadsafe(
                enviar_datos({"tipo": "flujo", "flujo_veh_h": flujo, "vehiculos_5min": vehiculos_5min}),
                loop_asyncio
            )
