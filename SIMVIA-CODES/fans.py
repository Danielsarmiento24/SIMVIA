import threading
import time
import logging

logger = logging.getLogger(__name__)

try:
    from rpi_hardware_pwm import HardwarePWM
    _PWM_AVAILABLE = True
except ImportError:
    _PWM_AVAILABLE = False
    logger.warning("rpi-hardware-pwm no disponible")


def _leer_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return float(f.read().strip()) / 1000.0
    except Exception:
        return 0.0


class FanController:
    CURVA = [(40, 0), (50, 30), (65, 60), (75, 85), (float("inf"), 100)]

    def __init__(self, dht_sensor=None):
        self._dht = dht_sensor
        self._velocidad = 0
        self._cpu_temp = 0.0
        self._manual = None  # None = auto, 0-100 = manual override
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._pwm1 = None
        self._pwm2 = None

        if not _PWM_AVAILABLE:
            logger.warning("FanController deshabilitado")
            return

        try:
            import subprocess
            subprocess.run(["pinctrl", "set", "12", "a0"], check=False)
            subprocess.run(["pinctrl", "set", "13", "a0"], check=False)
            self._pwm1 = HardwarePWM(pwm_channel=0, hz=25000, chip=0)
            self._pwm2 = HardwarePWM(pwm_channel=1, hz=25000, chip=0)
            self._pwm1.start(0)
            self._pwm2.start(0)
            print("Fans iniciados OK en chip=0 GPIO12/GPIO13")
        except Exception as e:
            logger.error(f"Error PWM fans: {e}")
            self._pwm1 = None
            self._pwm2 = None
            return

        threading.Thread(target=self._loop, daemon=True, name="fans").start()

    def _calcular_velocidad(self, cpu_temp):
        if self._dht is not None:
            temp_amb = self._dht.temperatura
            if temp_amb is not None:
                cpu_temp += max(0, (temp_amb - 25) * 0.3)
        for umbral, duty in self.CURVA:
            if cpu_temp < umbral:
                return duty
        return 100

    def set_manual(self, speed):
        """speed: 0-100 para manual, None para volver a auto."""
        with self._lock:
            self._manual = speed
            if speed is not None:
                self._velocidad = speed
        # Aplicar inmediatamente sin esperar el loop
        if speed is not None:
            if self._pwm1:
                self._pwm1.change_duty_cycle(speed)
            if self._pwm2:
                self._pwm2.change_duty_cycle(speed)

    def _loop(self):
        while not self._stop.is_set():
            cpu_temp = _leer_cpu_temp()
            with self._lock:
                manual = self._manual
            if manual is not None:
                velocidad = manual
            else:
                velocidad = self._calcular_velocidad(cpu_temp)
            with self._lock:
                self._cpu_temp = cpu_temp
                self._velocidad = velocidad
            if self._pwm1:
                self._pwm1.change_duty_cycle(velocidad)
            if self._pwm2:
                self._pwm2.change_duty_cycle(velocidad)
            time.sleep(5)

    @property
    def velocidad(self):
        with self._lock:
            return self._velocidad

    @property
    def cpu_temp(self):
        with self._lock:
            return self._cpu_temp

    @property
    def modo(self):
        with self._lock:
            return "manual" if self._manual is not None else "auto"

    def datos(self):
        with self._lock:
            return {
                "cpu_temp": round(self._cpu_temp, 1),
                "fan_pct": self._velocidad,
                "fan_modo": "manual" if self._manual is not None else "auto",
            }

    def detener(self):
        self._stop.set()
        for pwm in [self._pwm1, self._pwm2]:
            if pwm:
                try:
                    pwm.stop()
                except Exception:
                    pass
