from ventilation_settings import *
from humidity_settings import *

# API port
PORT = 9090

# Period in which worker will run and update state
ERRAND_PERIOD = 10

def get_init_hum_settings():
    # humidity range 80-90, wait_per - 1 hour, run_per - 2 minutes
    return HumiditySettings(80, 90, 3600, 120, "manual", False)

def get_init_vent_settings():
    # wait_per - 1 hour, run_per - 2 minutes
    return VentilationSettings(3600, 120, "manual", False)
