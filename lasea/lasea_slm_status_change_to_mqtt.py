#! /usr/bin/python3

import RPi.GPIO as GPIO 
import time, sys, json, copy, opcua_server

from my_mqtt_module import Mqtt

GPIO.setmode(GPIO.BCM)

# topics are set in config.yml file
  # topic_current_status = "diep2/lasea/stack_light/current_status" topic_status_changed = "diep2/lasea/stack_light/status_changed"

message = {"id":2, "timestamp":"", "payload": ""}

sensors = {
    "sensor1": {
        "color": "white",
        "pin": 3,
        "status": "False",
        "changes": 0,
        },
    "sensor2": {
        "color": "red",
        "pin": 4,
        "status": "False",
        "changes": 0,
        },
    "sensor3": {
        "color": "yellow",
        "pin": 17,
        "status": "False",
        "changes": 0,
        },
    "sensor4": {
        "color": "blue",
        "pin": 22,
        "status": "False",
        "changes": 0,
        },
    "sensor5": {
        "color": "green",
        "pin": 27,
        "status": "False",
        "changes": 0,
        },
    }

for s in sensors:
    GPIO.setup(sensors[s]["pin"], GPIO.IN)

def get_lamp_status():
    # read sensor values: looping through sensors and get inversed GPIO pin status
    for s in sensors:
        sensors[s]["status"] = str(not GPIO.input(sensors[s]["pin"]))
        # reset detected changes to zero
        sensors[s]["changes"] = 0

    # check the status every 0.25 sec during 3 secs and check per colour how many changes took place
        # if <1 change in 3 secs = not blinking if 1 change in 3 secs = possibly blinking --> check for two more seconds to make sure if >1 change in 5 secs = blinking
    sensors_previous = copy.deepcopy(sensors) # deepcopy function to copy all levels of dict without mixing the two dicts
    change_detected = False

    # loop 12 times * 0.25s to check during 3 secs and count changes
    for i in range(12):
        for s in sensors:
            sensors[s]["status"] = str(not GPIO.input(sensors[s]["pin"]))
            if sensors[s]["status"] != sensors_previous[s]["status"]:
                sensors[s]["changes"] += 1
        sensors_previous = copy.deepcopy(sensors)
        time.sleep(0.25)
    
    for s in sensors:
        if sensors[s]["changes"]>0:
            change_detected = True
    
    # if change detected look 2s longer for a second change being confirmation of blinking
    if change_detected:
        print("change detected")
        for i in range(8):
            for s in sensors:
                sensors[s]["status"] = str(not GPIO.input(sensors[s]["pin"]))
                if sensors[s]["status"] != sensors_previous[s]["status"]:
                    sensors[s]["changes"] += 1
            sensors_previous = copy.deepcopy(sensors)
            time.sleep(0.25)

    # if changes detected for one colour >1 then light is blinking
    for s in sensors:
        if sensors[s]["changes"]>1:
            sensors[s]["status"] = "blinking"
            print("sensor {} is {}.".format(sensors[s]["color"], sensors[s]["status"]))

    # extract color and status only
    sensors_status = {}
    for s in sensors:
        sensors_status[sensors[s]["color"]] = sensors[s]["status"]

    # create json object from color and status only
    payload = {"status": json.dumps(sensors_status)}
    payload_str = json.dumps(payload)
    return payload_str

def update_message():
    message["payload"] = get_lamp_status()
    message["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
#    mqtt_message = json.dumps(message)

def run(my_mqtt_config_yaml):
    try:
        mqtt = Mqtt(my_mqtt_config_yaml)
        mqtt.start()
        lamp_status_before = ""
        opcua_server.server.start()
        while True:
            update_message()
            opcua_server.myvar.set_value(json.dumps(message))
            if message["payload"] != lamp_status_before:
                print("change confirmed, publishing new status: {}".format(message))
                message_str = json.dumps(message)
                mqtt.publish(message_str)
                lamp_status_before = message["payload"]
            # no longer required to wait because getting the lamp status takes 3s at minimum time.sleep(mqtt.get_time_interval())
    finally:
        #close connection, remove subcsriptions, etc
        opcua_server.server.stop()

def main():
    # the yml config file is passed through from the service file which is calling
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)


if __name__ == "__main__":
    main()
