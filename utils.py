import utime
import network
from time_utils import sync_time, local_time_formatted
import sys

from sensor import *

def led_on_green(led):
    led[0] = (20, 0, 0)
    led.write()
    
def led_on_blue(led):
    led[0] = (0, 0, 20)
    led.write()
    
def led_on_red(led):
    led[0] = (0, 20, 0)
    led.write()
    
def led_off(led):
    led[0] = (0, 0, 0)
    led.write()

# Blinks the led
def blink(led, length):
    led_off(led)
    utime.sleep(length)
    led_on_green(led)
    utime.sleep(length)
    led_off(led)
    utime.sleep(length)

# Initial sequence - try out the sensors and connect to wifi
def init_sequence(main_led, log_manager):
    print(init_sensor(main_led))
    print(wifi_connect(main_led))
    try:
        sync_time()
        print("Time synced. Current time: " + local_time_formatted())
    except:
        log_manager.log_event("warning", "Time init failed", f"Time init failed, current time set to: {local_time_formatted()}")

# Connects to sensor - 10 tries
def init_sensor(main_led):
    sensor_data = None
    tries = 10
    while (sensor_data == None and tries > 0):
        tries -= 1
        blink(main_led, 0.25)
        try:
            sensor_data = get_sensor_data()
        except Exception as e:
            print("Failed to init sensor: ", e)
    if tries == 0:
        raise Exception("Failed to initialise sensor")
    
    return "Sensor initialised"

# Connects to wifi - 20 tries by default
def wifi_connect(main_led, tries = 20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected() and tries > 0:
        wlan.connect("Ateliér_2.4g", "3prstyvprdeli")
        tries -= 1
        blink(main_led, 1)
    
    if wlan.status() == network.STAT_GOT_IP:
        return "Wifi initialised - Got IP: " + str(wlan.ifconfig()[0])
    
    raise Exception("Failed to connect to wifi")

def log_exception(e: Exception):
    sys.print_exception(e)
    with open("error_log.txt", "a") as log_file:
        log_file.write("\nTime: {}\n".format(local_time_formatted()))
        sys.print_exception(e, log_file)
        log_file.write("\n-----\n")
