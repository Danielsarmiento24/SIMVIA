# SIMVIA / results — Resultados y Validación Experimental

Esta rama contiene los datos experimentales, métricas de validación y evidencias de las pruebas de campo realizadas con el prototipo SIMVIA.

---

## Estructura

```
results/
├── conteo_vehicular/
│   ├── datos_prueba_campo.csv         → Registros de conteo manual vs automático
│   ├── resumen_conteo.md              → Análisis de resultados de conteo
│   └── fotos/                         → Fotografías durante pruebas de campo
├── velocidad/
│   ├── datos_velocidad.csv            → Velocidad estimada vs referencia
│   └── resumen_velocidad.md           → Análisis de error de estimación
├── modelo/
│   ├── metricas_entrenamiento.csv     → Loss, mAP, precisión por época
│   ├── confusion_matrix.png           → Matriz de confusión
│   ├── PR_curve.png                   → Curva precisión-recall
│   └── F1_curve.png                   → Curva F1
├── operacion_continua/
│   ├── temperatura_log.csv            → Registro de temperatura durante operación
│   └── resumen_estabilidad.md         → Análisis de operación prolongada
└── impermeabilidad/
    ├── fotos_prueba_agua/             → Fotografías prueba de impermeabilidad
    └── resumen_ip.md                  → Análisis del grado de protección alcanzado
```

---

## Resultados principales

### Conteo vehicular

| Métrica | Resultado |
|---|---|
| Vehículos evaluados | ~200 |
| Método de referencia | Conteo manual simultáneo |
| Lugar de prueba | Puente peatonal — CC Cacique, Bucaramanga |
| Coincidencia con conteo manual | 100% |
| Condiciones evaluadas | Alto y bajo flujo, vehículos estacionados |

---

### Modelo de detección

| Métrica | Valor |
|---|---|
| Precisión final (mAP50) | ~90% |
| Clases detectadas | Automóvil, Motocicleta |
| Hardware de inferencia | Raspberry Pi 5 |
| Velocidad de inferencia | [completar — FPS en Raspberry Pi] |

---

### Estimación de velocidad

| Métrica | Valor |
|---|---|
| Método | Dos puntos de referencia físicos |
| Distancia entre puntos | [completar — metros] |
| Vehículos evaluados | [completar] |
| Instrumento de referencia | [completar — radar / GPS / video] |
| Error promedio | [completar — km/h o %] |

---

### Control térmico

| Condición | Temperatura registrada |
|---|---|
| Operación normal | [completar] |
| Operación prolongada (> X horas) | [completar] |
| Temperatura máxima registrada | [completar] |

---

### Prueba de impermeabilidad

| Aspecto | Resultado |
|---|---|
| Método | Exposición directa al agua con material absorbente interior |
| Resultado | Sin filtraciones detectadas |
| Protección alcanzada | IP6X (sellado al polvo) — [confirmar clasificación real] |

---

## Videos de pruebas

Los videos de campo están disponibles en:  
[Google Drive — Videos de Pruebas](https://drive.google.com/drive/folders/17pgdPkkZd47S0xBEOZMQ_ufsW0VNBBb1?usp=sharing)

| Video | Descripción |
|---|---|
| `prueba_conteo_alto_flujo.mp4` | Validación en hora pico |
| `prueba_conteo_bajo_flujo.mp4` | Validación en hora valle |
| `prueba_velocidad.mp4` | Estimación de velocidad en campo |
| `prueba_impermeabilidad.mp4` | Prueba de agua sobre la carcasa |
| `prueba_operacion_continua.mp4` | Funcionamiento durante periodo extendido |

---

## Lugar de pruebas

**Puente peatonal — Centro Comercial Cacique**  
Bucaramanga, Santander, Colombia

Las pruebas se realizaron en condiciones reales de tráfico urbano durante horarios de mañana y tarde para cubrir diferentes niveles de flujo vehicular.
