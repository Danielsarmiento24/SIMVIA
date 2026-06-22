# SIMVIA / hardware — Diseño Físico y Electrónico

Esta rama contiene todos los archivos relacionados con el diseño físico del prototipo SIMVIA: planos de la carcasa, esquemas electrónicos, lista de materiales y especificaciones de instalación.

---

## Estructura

```
hardware/
├── carcasa/
│   ├── planos/
│   │   ├── carcasa_v1.pdf        → Planos técnicos primera versión
│   │   └── carcasa_v2.pdf        → Planos técnicos versión final
│   ├── onshape/
│   │   └── enlace_onshape.md     → Enlace al modelo 3D en Onshape
│   └── fotos/
│       ├── version1/             → Fotografías primera versión fabricada
│       └── version2/             → Fotografías versión final
├── electronica/
│   ├── esquema_conexiones.pdf    → Diagrama de conexiones eléctricas
│   └── lista_componentes.md      → BOM (Bill of Materials)
└── instalacion/
    └── guia_instalacion.md       → Instrucciones de montaje en campo
```

---

## Especificaciones de la carcasa

| Característica | Valor |
|---|---|
| Material principal | Acero galvanizado |
| Dimensiones (L × A × H) | ~30 cm × 20 cm × 20–25 cm |
| Protección IP | IP65 (objetivo de diseño) |
| Sistema de fijación | Abrazaderas para poste o puente |
| Cubierta superior | Inclinada para evacuación de agua |
| Plataforma interna | Elevada ~3 cm sobre la base |
| Versiones fabricadas | 2 (iteración de diseño) |

---

## Lista de componentes principales (BOM)

| Componente | Cantidad | Función |
|---|---|---|
| Raspberry Pi 5 (8GB) | 1 | Unidad de procesamiento |
| Cámara | 1 | Captura de video |
| Sensor DHT11 | 1 | Temperatura y humedad interior |
| Ventilador Foxconn | 2 | Control térmico activo |
| Fuente de alimentación | 1 | Alimentación del sistema |
| Acero galvanizado | — | Carcasa exterior |

> Costo total del prototipo: aproximadamente **$1.401.668 COP**  
> Ver desglose completo en  [Google Drive — Anexos](https://drive.google.com/drive/folders/17pgdPkkZd47S0xBEOZMQ_ufsW0VNBBb1?usp=sharing)

---

## Evolución del diseño — v1 vs v2

### Versión 1 — Problemas identificados
- Pestaña de sellado subdimensionada (riesgo de filtración)
- Bisagras sobredimensionadas (peso excesivo)
- Aro de aseguramiento sobredimensionado

### Versión 2 — Correcciones aplicadas
- Rediseño completo del sistema de sellado
- Bisagras de perfil reducido
- Sistema de cierre optimizado en peso y estética

---
