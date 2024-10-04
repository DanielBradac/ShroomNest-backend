import machine
import json
import asyncio
import GPIO
import sys

from humidity_settings import *
from default_settings import *
from ip_settings import *
from utils import *
from sensor import *
from worker import *
from log_manager import *
from microdot import Microdot, Response
from neopixel import NeoPixel

# Humidity Settings init
hum_settings = get_init_hum_setting()

# IPSettings init
ip_settings = IPSettings()

# Log Manager
log_manager = LogManager()

# API routes
app = Microdot()

@app.get('/api/status') 
async def get_status(request):
    try:
        sensor_data = get_sensor_data()
        return json.dumps(sensor_data.serialize()), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return Response(None, 500, None, str(e))

@app.get('/api/getHumiditySettings') 
async def get_humidity_settings(request): 
    try:
        return json.dumps(hum_settings.serialize()), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return Response(None, 500, None, str(e))

@app.get('/api/getLogs') 
async def get_logs(request): 
    try:
        return json.dumps(log_manager.serialize()), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return Response(None, 500, None, str(e))

@app.post('/api/purgeLogs') 
async def purge_logs(request): 
    try:
        log_manager.purge_logs()
        return json.dumps(log_manager.serialize()), 200, {"Content-Type": "application/json"}
    except Exception as e:
        return Response(None, 500, None, str(e))
    
@app.post('/api/updateHumiditySettings') 
async def update_humidity_settings(request): 
    try:
        hum_settings.update_from_json(request.json, ip_settings.humidifier_ip, log_manager)
        return json.dumps(hum_settings.serialize()), 200, {"Content-Type": "application/json"}
    except ValueError as e:
        return Response(None, 400, None, str(e))
    except Exception as e:
        return Response(None, 500, None, str(e))
    
@app.post('/api/updateIPSettings') 
async def update_humidity_settings(request): 
    try:
        ip_settings.update_from_json(request.json)
        return json.dumps(ip_settings.serialize()), 200, {"Content-Type": "application/json"}
    except ValueError as e:
        return Response(None, 400, None, str(e))
    except Exception as e:
        return Response(None, 500, None, str(e))


# Function for periodical update
async def update_state(errand_per):
    try:
        # Init run
        run_errand(get_sensor_data(), hum_settings, ip_settings, log_manager, errand_per, True)
        while True:
            await asyncio.sleep(errand_per)
            run_errand(get_sensor_data(), hum_settings, ip_settings, log_manager, errand_per, False)
    except Exception as e:
        log_manager.log_event("error", "Errand ERROR", str(e))
        
# Main
async def main():
    background_task = asyncio.create_task(update_state(ERRAND_PERIOD))
    await app.start_server(port=PORT)

main_led = NeoPixel(machine.Pin(GPIO.RGB_PIN, machine.Pin.OUT), 1)

try:
    # Starting initial sequence, blink the led once and try out the sensor
    init_sequence(main_led, log_manager)
    # LED is turned on - everything is set up
    led_on_green(main_led)
    log_manager.log_event("info", "INIT Done", "INIT sequence done")
    # Start server
    asyncio.run(main())
    
except KeyboardInterrupt:
    print("Interrupted from keyboard")
    
except OSError as e:
    led_on_red(main_led)
    log_exception(e)
    # Probably wifi error, reboot device
    machine.reset()
    
except Exception as e:
    log_exception(e)
    
        
finally:
    # End of program, something went wrong - turn the led RED
    led_on_red(main_led)
