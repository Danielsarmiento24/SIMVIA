import json
import os
import time
import threading
from collections import deque

import config

conteo = {"auto": 0, "moto": 0, "bus": 0, "camion": 0}
ids_contados = set()
conteo_lock = threading.Lock()

timestamps_cruces = deque()
timestamps_lock = threading.Lock()

velocidades_ventana = deque()
velocidades_lock = threading.Lock()


def calcular_flujo():
    ahora = time.time()
    with timestamps_lock:
        while timestamps_cruces and ahora - timestamps_cruces[0] > config.VENTANA_FLUJO_SEG:
            timestamps_cruces.popleft()
        vehiculos_5min = len(timestamps_cruces)
    flujo = round((vehiculos_5min / config.VENTANA_FLUJO_SEG) * 3600)
    return flujo, vehiculos_5min


def calcular_vel_prom():
    ahora = time.time()
    with velocidades_lock:
        while velocidades_ventana and ahora - velocidades_ventana[0][0] > config.VENTANA_FLUJO_SEG:
            velocidades_ventana.popleft()
        vels = [v for _, v in velocidades_ventana]
    if not vels:
        return 0.0
    return round(sum(vels) / len(vels), 1)


def guardar_estado():
    with timestamps_lock:
        ts_list = list(timestamps_cruces)
    with conteo_lock:
        conteo_snap = dict(conteo)
    datos = {"conteo": conteo_snap, "timestamps_cruces": ts_list}
    tmp = config.ESTADO_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f)
    os.replace(tmp, config.ESTADO_FILE)


def cargar_estado():
    if not os.path.exists(config.ESTADO_FILE):
        return
    try:
        with open(config.ESTADO_FILE, "r") as f:
            datos = json.load(f)
        ahora = time.time()
        with conteo_lock:
            conteo.update(datos.get("conteo", {}))
        with timestamps_lock:
            for ts in datos.get("timestamps_cruces", []):
                if ahora - ts <= config.VENTANA_FLUJO_SEG:
                    timestamps_cruces.append(ts)
        print(f"Estado restaurado: {conteo}, {len(timestamps_cruces)} timestamps validos")
    except Exception as e:
        print(f"Error cargando estado: {e}")


def resetear():
    with conteo_lock:
        for k in conteo:
            conteo[k] = 0
        ids_contados.clear()
    with timestamps_lock:
        timestamps_cruces.clear()
