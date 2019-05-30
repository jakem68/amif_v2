#! /usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, json

from my_mqtt_module import Mqtt

GPIO.setmode(GPIO.BCM)

sensors = {
    "sensor1": {
        "color": "white",
        "pin": 3,
        "status": "False",
        },
    "sensor2": {
        "color": "red",
        "pin": 4,
        "status": "False",
        },
    "sensor3": {
        "color": "yellow",
        "pin": 17,
        "status": "False",
        },
    "sensor4": {
        "color": "blue",
        "pin": 22,
        "status": "False",
        },
    "sensor5": {
        "color": "green",
        "pin": 27,
        "status": "False",
        },
    }

for s in sensors:
    GPIO.setup(sensors[s]["pin"], GPIO.IN)

def get_lamp_status():
    # read sensor values: looping through sensors and get inversed GPIO pin status
    for s in sensors:
        sensors[s]["status"] = str(not GPIO.input(sensors[s]["pin"]))
#    return sensors

    sensors_status = {}
    for s in sensors:
        sensors_status[sensors[s]["color"]] = sensors[s]["status"]
    msg = {"status": json.dumps(sensors_status)}
    msg_out = json.dumps(msg)
    print(msg_out)
    return msg_out

def run(my_mqtt_config_yaml):
    mqtt = Mqtt(my_mqtt_config_yaml)
    mqtt.start()
    while True:
        lamp_status = get_lamp_status()
        mqtt.publish(lamp_status)
        time.sleep(mqtt.get_time_interval())

def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)


if __name__ == "__main__":
    main()
