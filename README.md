# SIMVIA — Sistema Inteligente de Monitoreo Vehicular

SIMVIA es un prototipo reproducible de monitoreo vehicular portátil basado en visión por computador e inteligencia artificial, diseñado para flujo vehicular en entornos urbanos con criterios de privacidad (no almacenamiento de imágenes) y operación en edge devices.

---

## Objetivo del repositorio
Proveer todo el soporte técnico y científico (código, hardware, modelos, datos, experimentos y documentación) necesario para reproducir y validar el sistema propuesto en la tesis: *Sistema Inteligente para Monitoreo Vehicular con Inteligencia Artificial*.

---

## Contenido principal
- `docs/` — Diagramas, metodología, normas y referencias académicas.
- `hardware/` — Esquemáticos, Detalles de hardware,  diseños de carcasa.
- `software/` — Código modular (edge, visión, comunicación, API, utilidades).
- `data/` — Datasets (raw, procesados), anotaciones y metadatos (política de privacidad).
- `models/` — Configuraciones y pesos (pretrained / entrenados) y scripts de conversión.
- `experiments/` — Experimentos documentados (objetivos, configuración, resultados).
- `results/` — Métricas, gráficas, tablas y logs reproducibles.
- `deployment/` — Guía de instalación en campo, configuración y mantenimiento.

---

## Mapa rápido para reproducibilidad
1. Revisar `docs/methodology/README.md`.  
2. Obtener datos (ver `data/README.md` y política de privacidad).  
3. Ejecutar entorno (ver `software/edge/README.md` y `software/vision/README.md`).  
4. Correr experimentos en `experiments/` (cada experimento incluye `notebook`).  
5. Resultados y métricas en `results/`.

---

## Requisitos (resumen)
- Python 3.8+ (entorno virtual recomendado).  
- Frameworks: PyTorch/TensorFlow según configuración del modelo (ver `models/configs/`).  
- Herramientas de edge: guías para Rapsberry Pi 5.  
- Dependencias en `software/requirements.txt`.

---
---

## Ética, privacidad y legalidad
- El proyecto evita almacenar imágenes o video por defecto.  


---

## Contacto
Autores: Daniel Felipe Sarmiento Pilonieta & Sebastian Adolfo Albornoz Villamil  
Director: Jeyson Arley Castillo Bohorquez  
Codirector:Jaime Guillermo Barrero Perez

---
