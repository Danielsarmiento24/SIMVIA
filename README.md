# SIMVIA —Sistema inteligente para monitoreo vehicular con inteligencia artificial

> Prototipo de monitoreo vehicular basado en inteligencia artificial y computación en el borde (Edge AI), desarrollado como Trabajo de Grado en la Escuela de Ingenierías Eléctrica, Electrónica y Telecomunicaciones — E3T, Universidad Industrial de Santander.

---

## ¿Qué es SIMVIA?

SIMVIA es un sistema embebido portátil capaz de detectar, clasificar y contar vehículos en tiempo real mediante visión computacional, sin almacenar imágenes ni videos. El procesamiento ocurre íntegramente en el dispositivo (Raspberry Pi 5), transmitiendo únicamente datos estadísticos agregados a una plataforma de visualización.

**Funciones principales:**
- Detección y clasificación vehicular en tiempo real (automóviles y motocicletas)
- Conteo vehicular mediante líneas virtuales de referencia
- Estimación de velocidad por puntos de referencia físicos
- Transmisión de datos a plataforma de visualización
- Carcasa en acero galvanizado con protección para intemperie

---

## Estructura del repositorio

```
SIMVIA/
├── docs/           → Informe final y documentación técnica
├── hardware/       → Planos de carcasa, esquemas eléctricos y lista de componentes
├── software/       → Código fuente del sistema (detección, conteo, velocidad, transmisión)
└── results/        → Métricas, pruebas de validación y datos experimentales
```

---

## Recursos complementarios

Los archivos de gran tamaño (videos de prueba, dataset completo, renders 3D) se encuentran en:

 **[Carpeta de Anexos en Google Drive](https://drive.google.com/drive/folders/17pgdPkkZd47S0xBEOZMQ_ufsW0VNBBb1?usp=sharing)**

Contenido de Drive:
- Videos de pruebas de campo (puente peatonal Centro Comercial Cacique)
- Dataset completo de entrenamiento
- Renders 3D de la carcasa (Onshape)
- Videos de pruebas de impermeabilidad y control térmico

---

## Hardware principal

| Componente | Descripción |
|---|---|
| Raspberry Pi 5 | Unidad de procesamiento principal (Edge AI) |
| Cámara | Captura de video en tiempo real |
| Sensor DHT11 | Monitoreo de temperatura interior |
| Ventiladores Foxconn | Control térmico activo |
| Carcasa acero galvanizado | Protección para instalación exterior |

---

## Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-orange)
![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry%20Pi%205-red)
![Roboflow](https://img.shields.io/badge/Dataset-Roboflow-purple)

---

## Ramas del repositorio

| Rama | Contenido |
|---|---|
| `main` | Rama principal — versión estable e integrada |
| `docs` | Informe LaTeX, figuras y documentación |
| `hardware` | Planos, esquemas y especificaciones físicas |
| `software` | Código fuente del sistema SIMVIA |
| `results` | Resultados experimentales y validaciones |

---

## Autores

**Daniel Felipe Sarmiento Pilonieta**  
**Sebastian Adolfo Albornoz Villamil**

### Dirección

- **Director:** Jeyson Arley Castillo Bohorquez  
- **Codirector:** Jaime Guillermo Barrero Perez  

### Institución

- **Universidad:** Universidad Industrial de Santander (UIS)  
- **Escuela:** E3T — Ingeniería Electrónica / Eléctrica / Telecomunicaciones  
- **Año:** 2026

---

## Licencia

Este proyecto fue desarrollado con fines académicos en la Universidad Industrial de Santander.  
Para uso o reproducción del sistema contactar a los autores.


---
