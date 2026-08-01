# Resultados crudos — evidencia de las métricas del informe


## Estructura

- `calibracion_conteo_yolo26n/` — calibración de conteo/clasificación con el modelo en producción (YOLO26n), 6 videos de referencia. Base de la Tabla de precisión inicial del informe.
- `calibracion_conteo_yolo11n_descartado/` — mismos 6 videos con YOLO11n, usado para la comparación que descartó este modelo.
- `calibracion_velocidad/Video N/` — validación de velocidad contra vehículo de referencia (velocímetro + GPS), 6 ubicaciones. Cada carpeta puede tener hasta 3 variantes:
  - `Video N_calibracion.json` — modelo de referencia (`best.pt`, PC).
  - `Video_N_calibracion_PI_NCNN.json` — mismo modelo exportado a NCNN, ejecutado en la Raspberry Pi (pre fine-tuning).
  - `Video_N_calibracion_PI_NCNN_finetuned.json` — modelo fine-tuneado (`yolo26n_cacique_ncnn_model`), NCNN en la Pi. Es la fuente de la Tabla 10 del informe (errores 0.5%–14.2%, Videos 1/2/3/6; Videos 4 y 5 descartados, ver notas en el informe).
- `benchmark_resultados.json` — FPS/latencia/RAM de 6 modelos NCNN (YOLOv8n/s, YOLOv9t, YOLOv10n, YOLO11n, YOLO26n), 100 frames cada uno. `detecciones_vehiculo: 0` en todos — la cámara no apuntaba a tráfico real durante esa corrida, cifra inválida; FPS/latencia sí son válidos.
- `benchmark_small_resultados.json` — FPS/latencia/RAM de YOLO26s y YOLO11s (variantes Small, sin fine-tuning), benchmark comparativo adicional pedido por el director de tesis.
