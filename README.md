# SIMVIA - Sistema Inteligente para el Monitoreo Vehicular con Inteligencia Artificial

## Descripción

Este repositorio contiene el código fuente y los archivos de desarrollo utilizados en el proyecto **SIMVIA (Sistema Inteligente para el Monitoreo Vehicular con Inteligencia Artificial)**.

El objetivo del proyecto es desarrollar un sistema portátil basado en visión por computador para el monitoreo del flujo vehicular, capaz de detectar y procesar información del tránsito utilizando una Raspberry Pi y otros dispositivos electrónicos.

Este repositorio corresponde a una rama de desarrollo donde se almacenan tanto los códigos utilizados durante la etapa de experimentación en Google Colab como la implementación realizada para la Raspberry Pi.

---

## Estructura del repositorio

```text
.
├── SIMVIA Codes/
│   ├── benchmark/
│   ├── calibrar/
│   ├── dht11/
│   ├── fans/
│   └── servidor/
│
├── notebooks y códigos de prueba (Google Colab)
└── demás archivos del proyecto
```

### Carpeta `SIMVIA Codes`

Contiene los programas utilizados durante la implementación del sistema en la Raspberry Pi.

* **benchmark/**
  Scripts para pruebas de rendimiento del sistema.

* **calibrar/**
  Herramientas para la calibración del sistema de visión.

* **dht11/**
  Código para la adquisición de datos del sensor de temperatura y humedad DHT11.

* **fans/**
  Control de los ventiladores del sistema de refrigeración.

* **servidor/**
  Código relacionado con la comunicación y los servicios del sistema.

---

## Código de desarrollo

Además del código para Raspberry Pi, esta rama incluye los diferentes scripts y notebooks utilizados durante las pruebas realizadas en Google Colab para el desarrollo y validación del sistema de visión por computador.

---

## Aplicación móvil

Debido al tamaño del archivo, el APK de la aplicación móvil no pudo incluirse en este repositorio.

La aplicación, junto con una copia de los archivos presentes en esta rama, se encuentra disponible en el siguiente enlace de Google Drive:

**Google Drive:**
https://drive.google.com/drive/folders/1zFFVwwUpDTDrV12DXUrM64vOX4AuEEjR?usp=sharing

---

## Requisitos generales

El proyecto fue desarrollado utilizando tecnologías como:

* Raspberry Pi
* Python
* OpenCV
* Modelos de visión por computador
* Google Colab
* Sensores ambientales (DHT11)

Dependiendo del módulo utilizado, pueden requerirse librerías adicionales.

---

## Estado del proyecto

Este repositorio corresponde a una versión de desarrollo del proyecto SIMVIA y contiene los diferentes componentes implementados durante el proceso de investigación y construcción del prototipo.

