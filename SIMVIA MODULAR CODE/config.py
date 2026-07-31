import json
import os
import threading

CONFIG_FILE = "/home/pi/trafico/config.json"
LOG_FILE = "/home/pi/trafico/flujo_log.csv"
ESTADO_FILE = "/home/pi/trafico/estado.json"

DISTANCIA_REAL_METROS = 8.0
LINEA_A_Y = 237
LINEA_B_Y = 337
LINEA_X_MIN = 0
CONFIANZA_MIN = 0.5
CONFIANZA_MIN_MOTO = 0.25
VEHICULOS = {0: "auto", 1: "bus", 2: "camion", 3: "moto"}
QUEUE_SIZE = 2
VENTANA_FLUJO_SEG = 300
INTERVALO_LOG_SEG = 30
SHEETS_URL = "https://script.google.com/macros/s/AKfycbwB_z1p5-BUyppxL5TUDXRXwlnRm31EU763JrnoyU2CBi1YSpIr0zjfYOj22U4wNWzhqQ/exec"

config_lock = threading.Lock()


def cargar_config():
    global DISTANCIA_REAL_METROS, LINEA_A_Y, LINEA_B_Y, LINEA_X_MIN
    if not os.path.exists(CONFIG_FILE):
        guardar_config()
        return
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        with config_lock:
            DISTANCIA_REAL_METROS = float(cfg.get("distancia", DISTANCIA_REAL_METROS))
            LINEA_A_Y = int(cfg.get("linea_a_y", LINEA_A_Y))
            LINEA_B_Y = int(cfg.get("linea_b_y", LINEA_B_Y))
            LINEA_X_MIN = int(cfg.get("linea_x_min", LINEA_X_MIN))
        print(f"Config cargada: dist={DISTANCIA_REAL_METROS}m, A={LINEA_A_Y}, B={LINEA_B_Y}, X_MIN={LINEA_X_MIN}")
    except Exception as e:
        print(f"Error cargando config: {e}")


def guardar_config():
    with config_lock:
        cfg = {
            "distancia": DISTANCIA_REAL_METROS,
            "linea_a_y": LINEA_A_Y,
            "linea_b_y": LINEA_B_Y,
            "linea_x_min": LINEA_X_MIN,
        }
    tmp = CONFIG_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, indent=2)
    os.replace(tmp, CONFIG_FILE)
    print(f"Config guardada: dist={cfg['distancia']}m, A={cfg['linea_a_y']}, B={cfg['linea_b_y']}, X_MIN={cfg['linea_x_min']}")


def actualizar(distancia, linea_a_y, linea_b_y, linea_x_min):
    global DISTANCIA_REAL_METROS, LINEA_A_Y, LINEA_B_Y, LINEA_X_MIN
    with config_lock:
        DISTANCIA_REAL_METROS = float(distancia)
        LINEA_A_Y = int(linea_a_y)
        LINEA_B_Y = int(linea_b_y)
        LINEA_X_MIN = int(linea_x_min)
    guardar_config()


def snapshot():
    with config_lock:
        return {
            "distancia": DISTANCIA_REAL_METROS,
            "linea_a_y": LINEA_A_Y,
            "linea_b_y": LINEA_B_Y,
            "linea_x_min": LINEA_X_MIN,
        }
