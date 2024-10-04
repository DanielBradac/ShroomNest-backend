from humidity_settings import *

# API port
PORT = 9090

# Period in which worker will run and update state
ERRAND_PERIOD = 10

def get_init_hum_setting():
    # humidity range 80-90, wait_per - 2 hours, run_per - 2
    return HumiditySettings(80, 90, 3600, 120, "manual", False)
