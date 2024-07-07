import machine
import utime
import network

from sensor import *

# Blinks the diod
def blink(led, length):
    led.off()
    utime.sleep(length)
    led.on()
    utime.sleep(length)
    led.off()
    utime.sleep(length)

# Initial sequence - try out the sensors and connect to wifi
def init_sequence(main_led):
    print(init_sensor(main_led))
    print(wifi_connect(main_led))

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
        return "Got IP: " + str(wlan.ifconfig()[0])
    
    raise Exception("Failed to connect to wifi") 
