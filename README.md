# SIMVIA / Results — Resultados y Validación Experimental

Esta rama contiene los resultados experimentales obtenidos durante el desarrollo y validación del proyecto **SIMVIA (Sistema Inteligente para el Monitoreo Vehicular con Inteligencia Artificial)**.

Aquí se almacenan las evidencias utilizadas para evaluar el desempeño del sistema, incluyendo pruebas de entrenamiento de modelos, métricas de detección, validación del conteo vehicular, estimación de velocidad, pruebas sobre Raspberry Pi 5 y demás resultados obtenidos durante el proceso de investigación.

---

## Objetivo

El propósito de esta rama es centralizar toda la evidencia experimental del proyecto, permitiendo documentar y respaldar las decisiones de diseño adoptadas durante el desarrollo de SIMVIA.

Los resultados aquí presentados fueron utilizados para:

* Seleccionar el sistema embebido del prototipo.
* Seleccionar la arquitectura de inteligencia artificial.
* Evaluar el desempeño de los modelos entrenados.
* Validar el sistema de conteo vehicular.
* Validar el sistema de clasificación vehicular.
* Validar el sistema de estimación de velocidad.
* Analizar el desempeño computacional sobre Raspberry Pi 5.
* Documentar las mejoras implementadas durante el proceso de desarrollo.


---

## Evaluación de modelos de inteligencia artificial

Durante el desarrollo de SIMVIA se realizaron múltiples pruebas comparativas entre diferentes arquitecturas de detección de objetos basadas en la familia YOLO.

Las evaluaciones consideraron criterios relevantes para sistemas embebidos:

* Precisión de detección (mAP50-95).
* Porcentaje de captura vehicular.
* F1-Score.
* Velocidad de inferencia (FPS).
* Latencia.
* Consumo de recursos computacionales.
* Comportamiento sobre Raspberry Pi 5.

Las pruebas fueron ejecutadas inicialmente en Google Colab y posteriormente sobre la Raspberry Pi 5 bajo condiciones equivalentes de evaluación.

---

## Dataset utilizado

Para el entrenamiento de los modelos se empleó un conjunto de datos desarrollado en Roboflow.

Características principales:

* Dataset original: 998 imágenes.
* Clase inicial: Vehículo.
* Aplicación de técnicas de Data Augmentation.
* Dataset final: 2238 imágenes.

Distribución utilizada:

| Conjunto      | Cantidad |
| ------------- | -------: |
| Entrenamiento |     2083 |
| Validación    |      200 |
| Prueba        |      100 |

Las imágenes fueron sometidas a procesos de aumento de datos que incluyeron:

* Rotaciones.
* Volteo horizontal y vertical.
* Desenfoque controlado.
* Corrección automática de orientación.
* Redimensionamiento a 640 × 640 píxeles.

---

## Selección del modelo

Los modelos con mejor desempeño fueron comparados mediante métricas experimentales homogéneas.

### Comparación de arquitecturas

| Modelo  | mAP50-95 | Captura (%) |     F1 |   FPS |
| ------- | -------: | ----------: | -----: | ----: |
| YOLO26 |   0.6309 |       90.48 | 0.9236 | 74.14 |
| YOLOv8 |   0.6235 |       92.15 | 0.9305 | 62.85 |
| YOLO11 |   0.6174 |       91.38 | 0.9335 | 74.19 |

Los resultados mostraron que la arquitectura **YOLO26** ofrecía el mejor equilibrio entre precisión, velocidad de procesamiento y eficiencia computacional para su implementación en sistemas embebidos.

Por esta razón fue seleccionada como arquitectura base del sistema SIMVIA.

---

## Modelo desplegado

Aunque la comparación principal se realizó utilizando versiones Small de cada arquitectura, para el despliegue final se utilizó:

**YOLO26n (Nano)**

Exportado al formato:

**NCNN**

La selección de esta versión permitió:

* Reducir el consumo de memoria.
* Disminuir la carga computacional.
* Mantener inferencia en tiempo real.
* Mejorar la viabilidad operativa sobre Raspberry Pi 5.

---

## Validación del sistema de conteo vehicular

La validación se realizó mediante comparación directa entre:

* Conteo manual de referencia.
* Conteo generado automáticamente por SIMVIA.

Resultados iniciales:

| Métrica                  |  Valor |
| ------------------------ | -----: |
| Vehículos analizados     |    135 |
| Vehículos detectados     |    103 |
| Precisión global inicial | 76.3 % |

Posteriormente se aplicaron ajustes relacionados con:

* Umbrales de confianza.
* Calibración de líneas virtuales.
* Exclusión de zonas de parqueo.
* Optimización del seguimiento vehicular.

Después de la calibración se alcanzaron precisiones superiores al 90 % en múltiples escenarios de prueba.

---

## Validación de clasificación vehicular

El sistema fue diseñado para clasificar:

* Automóvil.
* Motocicleta.
* Bus.
* Camión.

Durante las pruebas se identificó que la categoría motocicleta presentaba el mayor nivel de dificultad debido a:

* Menor tamaño relativo dentro de la imagen.
* Mayor variabilidad visual.
* Oclusiones frecuentes.

Como resultado del reentrenamiento y ajuste de parámetros:

* El recall de motocicletas aumentó aproximadamente de 24 % a 58 %.
* Se mejoró significativamente la capacidad de clasificación de esta categoría.

---

## Validación de estimación de velocidad

La velocidad se calcula mediante el tiempo requerido para que un vehículo recorra una distancia conocida entre dos líneas virtuales de referencia.

Las pruebas de validación utilizaron vehículos de referencia con velocidades verificadas mediante:

* Velocímetro del vehículo.
* Aplicaciones de navegación satelital.

### Resultados obtenidos

| Velocidad real | Velocidad estimada | Error   |
| -------------- | ------------------ | ------- |
| 40 km/h        | 43.1 km/h          | +7.8 %  |
| 44 km/h        | 44.2 km/h          | +0.5 %  |
| 48 km/h        | 49.2 km/h          | +2.5 %  |
| 43 km/h        | 36.9 km/h          | -14.2 % |

Los errores observados estuvieron asociados principalmente a:

* Oclusiones entre vehículos.
* Reasignación de identificadores durante el seguimiento.
* Configuraciones de calibración específicas del sitio de instalación.

---

## Desempeño sobre Raspberry Pi 5

Se evaluó el comportamiento de diferentes modelos exportados al formato NCNN para inferencia local.

### Velocidad de inferencia

| Modelo         |  FPS |
| -------------- | ---: |
| YOLO26n (NCNN) | 55.9 |
| YOLO11n (NCNN) | 53.5 |

Los resultados demostraron la capacidad de la Raspberry Pi 5 para ejecutar inferencia en tiempo real sin necesidad de aceleradores externos.

---

## Principales hallazgos

Durante el proceso de validación se identificaron varios aspectos relevantes:

* La precisión del sistema depende significativamente de la calibración realizada para cada sitio de instalación.
* Las oclusiones vehiculares afectan principalmente el algoritmo de seguimiento y no el modelo de detección.
* El procesamiento en el borde (Edge AI) es viable utilizando Raspberry Pi 5.
* El formato NCNN permite una ejecución eficiente de modelos YOLO en hardware embebido.
* La arquitectura YOLO26 ofreció el mejor equilibrio entre precisión y rendimiento para los objetivos del proyecto.
* El sistema alcanzó niveles adecuados de desempeño para aplicaciones de monitoreo vehicular en tiempo real.

---

## Evidencia experimental

Esta rama puede incluir:

* Curvas de aprendizaje.
* Curvas Precision-Recall.
* Resultados de entrenamiento.
* Matrices de confusión.
* Gráficos de métricas.
* Capturas de inferencia.
* Videos de validación.
* Reportes experimentales.
* Archivos generados por Roboflow y Ultralytics.
* Resultados obtenidos en Raspberry Pi 5.

---

## Repositorio de respaldo

Debido a las limitaciones de almacenamiento de GitHub, algunos archivos de gran tamaño pueden encontrarse únicamente en Google Drive.

El repositorio de respaldo contiene:

* Los mismos archivos presentes en esta rama.
* Videos de validación.
* Resultados completos de entrenamiento.
* Modelos entrenados.
* Evidencias experimentales adicionales.
* Archivos que exceden los límites de GitHub.

### Google Drive

[[Repositorio de Google Drive]](https://drive.google.com/drive/folders/17pgdPkkZd47S0xBEOZMQ_ufsW0VNBBb1?usp=sharing)

---

## Relación con el proyecto

Los resultados almacenados en esta rama corresponden a la evidencia experimental utilizada en el documento:

**"Sistema Inteligente para Monitoreo Vehicular con Inteligencia Artificial (SIMVIA)"**

desarrollado en la Universidad Industrial de Santander como parte del trabajo de grado de pregrado en Ingeniería Electrónica.
