#! /usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, json

from my_mqtt_module import mqtt_publish, time_interval

GPIO.setmode(GPIO.BCM)

sensors_on_pin = {"sensor1": 3, "sensor2": 4,"sensor3": 17,"sensor4": 27}
sensors = {
    "sensor1": {
        "color": "red",
        "pin": 3,
        "status": False,
        },
    "sensor2": {
        "color": "green",
        "pin": 4,
        "status": False,
        },
    "sensor3": {
        "color": "yellow",
        "pin": 17,
        "status": False,
        },
    "sensor4": {
        "color": "blue",
        "pin": 27,
        "status": False,
        },
    }
# loop through pins to set them as DIG IN
#for s in sensors_on_pin:
#    GPIO.setup(sensors_on_pin[s],GPIO.IN)

for s in sensors:
    GPIO.setup(sensors[s]["pin"], GPIO.IN)

def get_lamp_status():
    # read sensor values: looping through sensors and get inversed GPIO pin status
    for s in sensors:
        sensors[s]["status"] = not GPIO.input(sensors[s]["pin"])
    return sensors

def send_to_tb(sensors):
    msg = {"status": str(sensors)}
    msg_out = json.dumps(msg)
    print(msg_out)
    mqtt_publish(msg_out = msg_out)


def main():
    while True:
        sensors = get_lamp_status()
        send_to_tb(sensors)
        time.sleep(time_interval)
	

if __name__ == "__main__":
    main()
