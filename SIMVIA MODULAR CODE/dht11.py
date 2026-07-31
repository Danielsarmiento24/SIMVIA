import threading
import time
import logging

logger = logging.getLogger(__name__)

try:
    import board
    import adafruit_dht
    _DHT_AVAILABLE = True
except ImportError:
    _DHT_AVAILABLE = False
    logger.warning("adafruit-circuitpython-dht no instalado")


class DHT11Sensor:
    INTERVALO = 3.0

    def __init__(self, pin=None):
        self._temp = None
        self._hum = None
        self._ok = False
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._device = None

        if not _DHT_AVAILABLE:
            logger.warning("DHT11 deshabilitado")
            return

        if pin is None:
            pin = board.D4

        try:
            self._device = adafruit_dht.DHT11(pin, use_pulseio=False)
        except Exception as e:
            logger.error(f"No se pudo inicializar DHT11: {e}")
            return

        print("DHT11 iniciado OK en GPIO4")
        threading.Thread(target=self._loop, daemon=True, name="dht11").start()

    def _loop(self):
        while not self._stop.is_set():
            self._leer()
            time.sleep(self.INTERVALO)

    def _leer(self):
        if self._device is None:
            return
        try:
            temp = self._device.temperature
            hum = self._device.humidity
            if temp is not None and hum is not None:
                with self._lock:
                    self._temp = temp
                    self._hum = hum
                    self._ok = True
        except RuntimeError:
            with self._lock:
                self._ok = False
        except Exception as e:
            logger.error(f"Error DHT11: {e}")
            with self._lock:
                self._ok = False

    @property
    def temperatura(self):
        with self._lock:
            return self._temp

    @property
    def humedad(self):
        with self._lock:
            return self._hum

    @property
    def ok(self):
        with self._lock:
            return self._ok

    def datos(self):
        with self._lock:
            return {"temp_ambiente": self._temp, "humedad": self._hum, "dht11_ok": self._ok}

    def detener(self):
        self._stop.set()
        if self._device:
            try:
                self._device.exit()
            except Exception:
                pass
