# SIMVIA / software — Código Fuente del Sistema

Esta rama contiene el código fuente completo del sistema SIMVIA: detección vehicular, conteo, estimación de velocidad, clasificación y transmisión de datos.

---

## Estructura

```
software/
├── src/
│   ├── main.py                   → Punto de entrada del sistema
│   ├── detector.py               → Módulo de detección YOLO
│   ├── tracker.py                → Módulo de seguimiento de objetos
│   ├── counter.py                → Módulo de conteo vehicular (líneas virtuales)
│   ├── speed_estimator.py        → Módulo de estimación de velocidad
│   ├── classifier.py             → Módulo de clasificación vehicular
│   └── transmitter.py            → Módulo de transmisión de datos
├── config/
│   ├── config.yaml               → Configuración general del sistema
│   └── camera_config.yaml        → Parámetros de cámara y puntos de referencia
├── utils/
│   ├── visualization.py          → Funciones de visualización (bounding boxes, líneas)
│   └── logger.py                 → Sistema de registro de eventos
├── tests/
│   └── test_counter.py           → Pruebas unitarias del contador
├── requirements.txt              → Dependencias del proyecto
└── setup.sh                      → Script de instalación en Raspberry Pi
```

---

## Requisitos del sistema

**Hardware:**
- Raspberry Pi 5 (recomendado 8 GB RAM)
- Cámara compatible (USB o CSI)
- Conexión a internet (para transmisión de datos)

**Software:**
```
Python 3.10+
ultralytics >= 8.0
opencv-python >= 4.8
numpy
pyyaml
requests  # o paho-mqtt según protocolo usado
```

---

## Instalación

```bash
# 1. Clonar solo esta rama
git clone --branch software https://github.com/tu-usuario/SIMVIA.git
cd SIMVIA

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar parámetros del sistema
nano config/config.yaml

# 4. Ejecutar el sistema
python src/main.py
```

---

## Configuración de puntos de referencia

Los puntos de referencia para conteo y velocidad se definen en `config/camera_config.yaml`:

```yaml
reference_points:
  point_a: [x1, y1]   # Punto de entrada (píxeles)
  point_b: [x2, y2]   # Punto de salida (píxeles)
  real_distance_m: 5.0 # Distancia física real entre puntos (metros)

counting_line:
  y_position: 300      # Posición vertical de la línea de conteo
```

---

## Modelo utilizado

El modelo entrenado (archivo `.pt`) se encuentra en la rama `models`.  
Descargar y colocar en `software/models/simvia_model.pt` antes de ejecutar.

---

## Transmisión de datos

**[COMPLETAR]** — Protocolo utilizado, endpoint, estructura del payload JSON.

---

## Funcionamiento general

```
Cámara → Frame → YOLO (detección) → Tracker (seguimiento)
       → Counter (conteo por línea virtual)
       → Speed Estimator (velocidad por puntos de referencia)
       → Classifier (categoría: automóvil / motocicleta)
       → Transmitter (envío a plataforma)
       → Visualizer (dashboard web)
```
