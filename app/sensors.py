try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
import time

class growbme280:
    def __init__(self):
        self.bus = SMBus(1)
        self.sensor = BME280(i2c_dev=self.bus, i2c_addr=0x76)

    def get_readings(self):
        # Ignore first result since it seems stale
        temperature = self.sensor.get_temperature()
        pressure = self.sensor.get_pressure()
        humidity = self.sensor.get_humidity()
        time.sleep(0.1)

        temperature = self.sensor.get_temperature()
        pressure = self.sensor.get_pressure()
        humidity = self.sensor.get_humidity()
        time_str = time.strftime("%H:%M:%S")

        return {
            "time": time_str,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity
        }
