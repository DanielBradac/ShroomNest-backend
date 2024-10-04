import GPIO

from BME280 import BME280
from machine import Pin, I2C

# Data class for data pulled out of sensor
class SensorData:
    def __init__(self, temperature: float, humidity: float):
        self.temperature = temperature
        self.humidity = humidity
        
    def serialize(self):
        return {
            "temperature": self.temperature, "humudity": self.humidity
        }

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(GPIO.D1), sda=Pin(GPIO.D0), freq=10000)
bme = BME280(i2c=i2c)

# Function reads temperature and humidity from sensor
def get_sensor_data():
    return SensorData(bme.temperature, bme.humidity)
