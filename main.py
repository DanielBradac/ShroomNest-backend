import machine
import json
import asyncio

from humidity_settings import *
from ip_settings import *
from utils import *
from sensor import *
from worker import *
from log_manager import *
from microdot import Microdot, Response

# Humidity Settings init
hum_settings = HumiditySettings(80, 90, "auto", False)

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
        hum_settings.update_from_json(request.json, ip_settings.humidifier_ip)
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
async def update_state(period):
    # Init run
    run_errand(get_sensor_data(), hum_settings, ip_settings, log_manager, True)
    while True:
        await asyncio.sleep(period)
        run_errand(get_sensor_data(), hum_settings, ip_settings, log_manager, False)
        
# Main
async def main():
    background_task = asyncio.create_task(update_state(10))
    await app.start_server(port=9090)

try:
    main_led = machine.Pin("LED", machine.Pin.OUT)

    # Starting initial sequence, blink the led once and try out the sensor
    init_sequence(main_led)
    # LED is turned on - everything is set up
    main_led.on()
    # Start server
    asyncio.run(main())
    
except KeyboardInterrupt:
    print("Interrupted from keyboard")
except Exception as e:
    print("Error: ", e)
finally:
    # End of program - turn the led off
    main_led.off()
