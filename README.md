# SIMVIA / docs — Documentación e Informe Final

Esta rama contiene la documentación técnica completa del proyecto SIMVIA, incluyendo el informe final de trabajo de grado en formato LaTeX y los recursos gráficos asociados.

---

## Estructura

```
docs/
├── informe/
│   ├── main.tex                  → Archivo principal del informe
│   ├── capitulo1_intro.tex       → Introducción
│   ├── capitulo2_marco.tex       → Marco Teórico (Conceptos Previos)
│   ├── capitulo3_desarrollo.tex  → Desarrollo de la Solución
│   ├── capitulo4_conclusiones.tex
│   ├── capitulo5_recomendaciones.tex
│   └── referencias.bib           → Referencias bibliográficas (APA)
├── figuras/
│   ├── arquitectura/             → Diagramas de arquitectura del sistema
│   ├── carcasa/                  → Renders e imágenes de la carcasa
│   ├── pruebas/                  → Capturas de pantalla de pruebas
│   └── yolo/                     → Gráficas de entrenamiento del modelo
├── tablas/
│   └── tablas_capitulo2.tex      → Tablas de comparación (LaTeX)
└── matrices/
    ├── matriz1_seleccion_yolo.png
    ├── matriz2_plataforma_edge.png
    └── matriz3_algoritmo_tracking.png
```

---

## Compilación del informe en Overleaf

1. Descarga o clona esta rama
2. Sube la carpeta `informe/` a un nuevo proyecto en [Overleaf](https://overleaf.com)
3. Establece `main.tex` como documento principal
4. Compila con **pdfLaTeX**

**Paquetes requeridos** (incluidos en Overleaf por defecto):
```
booktabs, array, float, graphicx, hyperref, inputenc, babel (spanish)
```

---

## Recursos de gran tamaño

Los videos de demostración y el PDF final compilado se encuentran en:

**[Google Drive — Anexos SIMVIA](https://drive.google.com/drive/folders/17pgdPkkZd47S0xBEOZMQ_ufsW0VNBBb1?usp=sharing)**

---

## Normas aplicadas

El informe sigue las directrices de la **Guía para la Elaboración del Informe Final de Trabajo de Grado — E3T (versión 2024-II)**, incluyendo:
- Extensión máxima de 40 páginas (sin anexos)
- Normas de citación APA
- Fuente Arial 11pt, interlineado 1.5
