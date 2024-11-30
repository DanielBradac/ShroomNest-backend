# App description
MicroPython server for monitoring state and adjusting humidity and ventilation inside of a grow tent.

# Hardware requirements
* ESP32-S3 micochip with MicroPython v1.19+
* BME280 humidity and temperature sensor

# Features:
- REST API
- Logging on three levels - info, warning, error
- Humidity management modes
  - Manual (ON/OFF)
  - Automatic - keeps set humidity range
  - Periodic - turns humidifier on and off after set *run* and *wait* periods
- Ventilation management
  - Manual (ON/OFF)
  - Periodic - turns fans on and off after set *run* and *wait* periods

# API endpoints
* /status - current temperature and humidity from BME280
* /getHumiditySettings - current humidity manager setting and humimdifier state (ON/OFF)
* /getVentilationSettings - current ventilation manager setting and fans state (ON/OFF)
* /getLogs - info, warning and error logs with timestamps
* /purgeLogs - deletes logs
* /updateHumiditySettings - updates humidity manager settings
* /updateVentilationSettings - updates ventilation manager settings
* /updateIPSettings - updates samrt socket ip settings
