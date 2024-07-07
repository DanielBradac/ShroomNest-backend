import dht
import machine

# Data class for data pulled out of sensor
class SensorData:
    def __init__(self, temperature: float, humidity: float):
        self.temperature = temperature
        self.humidity = humidity
        
    def serialize(self):
        return {
            "temperature": self.temperature, "humudity": self.humidity
        }

# Function reads temperature and humidity from sensor
def get_sensor_data():
    sensor = dht.DHT22(machine.Pin(28))
    sensor.measure()
    return SensorData(sensor.temperature(), sensor.humidity())