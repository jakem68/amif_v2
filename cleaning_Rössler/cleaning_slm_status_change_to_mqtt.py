#! /usr/bin/python3

import RPi.GPIO as GPIO 
import time, sys, json, copy, opcua_server, threading

from my_mqtt_module import Mqtt

GPIO.setmode(GPIO.BCM)

# topics are set in config.yml file
  # topic_current_status = "diep2/lasea/stack_light/current_status" topic_status_changed = "diep2/lasea/stack_light/status_changed"

message = {"id":2, "timestamp":"", "payload": ""}

sensors = {
#    "sensor1": {"color": "white","pin": 3,"value": False,"status": "off","changes": 0,},
    "sensor2": {"color": "red","pin": 4,"value": False,"status": "off","changes": 0,},
    "sensor3": {"color": "yellow","pin": 17,"value": False,"status": "off","changes": 0,},
#    "sensor4": {"color": "blue","pin": 22,"value": False,"status": "off","changes": 0,},
    "sensor5": {"color": "green","pin": 27,"value": False,"status": "off","changes": 0,},
    }

# initialize pins as Inputs
for s in sensors:
    GPIO.setup(sensors[s]["pin"], GPIO.IN)

def update_sensor_values():
    # read sensor values: looping through sensors and get inversed GPIO pin value
    for s in sensors:
        sensors[s]["value"] = str(not GPIO.input(sensors[s]["pin"]))

def reset_sensor_changes():
    for s in sensors:
        sensors[s]["changes"] = 0

def return_changed_colors(sensor_dict_one, sensor_dict_two):
    changed_colors = []
    for s in sensor_dict_one:
        if sensor_dict_one[s]["value"] != sensor_dict_two[s]["value"]:
            changed_colors.append(sensor_dict_one[s]["color"])
    return changed_colors

# count changes per colour to determine whether blinking or not
def add_changes_per_color(changed_colors):
    for s in sensors:
        if sensors[s]["color"] in changed_colors:
            sensors[s]["changes"] += 1

def check_for_blinking():
    # loop 18 times * 0.25s to check during 4.5 secs and count changes
    blinking = False
    for i in range(18):
        sensors_previous = copy.deepcopy(sensors)
        time.sleep(0.25)
        update_sensor_values()
        changed_colors = return_changed_colors(sensors_previous, sensors)
        add_changes_per_color(changed_colors)
        changed_colors = []
    for s in sensors:
        if sensors[s]["changes"]>1:
            blinking = True
    return blinking

# update the status in the sensors dictionary and reset the sensor_changes dictionary
def update_sensors_status():
    for s in sensors:
        if sensors[s]["changes"]>1:
            sensors[s]["status"] = "blinking"
            # print("sensor {} is {}.".format(sensors[s]["color"], sensors[s]["status"]))
        elif sensors[s]["value"] == "True":
            sensors[s]["status"] = "on"
        else:
            sensors[s]["status"] = "off"
    reset_sensor_changes()

def get_lamp_status():
    # extract color and status only
    sensors_status = {}
    for s in sensors:
        sensors_status[sensors[s]["color"]] = sensors[s]["status"]
    return sensors_status

def update_mqtt_message():
    message["payload"] = get_lamp_status()
    message["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')

def run_opcua():
    opcua_server.server.start()
    while True:
        opcua_update()
        time.sleep(1)

def opcua_update():
    for s in sensors:
        value = sensors[s]["value"]
        status = sensors[s]["status"]
        switcher.get(sensors[s]["color"])(value, status)
    opcua_update_slm()

def opcua_update_green(value, status):
    opcua_server.green_value.set_value(value)
    opcua_server.green_status.set_value(status)
    # print("green, {}, {}".format(value, status))

def opcua_update_red(value, status):
    opcua_server.red_value.set_value(value)
    opcua_server.red_status.set_value(status)
    # print("red, {}, {}".format(value, status))

def opcua_update_yellow(value, status):
    opcua_server.yellow_value.set_value(value)
    opcua_server.yellow_status.set_value(status)
    # print("yellow, {}, {}".format(value, status))

def opcua_update_blue(value, status):
    opcua_server.blue_value.set_value(value)
    opcua_server.blue_status.set_value(status)
    # print("blue, {}, {}".format(value, status))

def opcua_update_white(value, status):
    opcua_server.white_value.set_value(value)
    opcua_server.white_status.set_value(status)
    # print("white, {}, {}".format(value, status))

# updates the general status of the slm being the status of the most critical color which is active
def opcua_update_slm():
    active_sensors = []
    highest_color = ""
    slm_status = ""
    for s in sensors:
        if sensors[s]["status"] != "off":
            active_sensors.append(sensors[s]["color"])
    # look for most important active sensor
    if active_sensors != []:
        if "red" in active_sensors:
            highest_color = "red"
        elif "yellow" in active_sensors:
            highest_color = "yellow"
        elif "blue" in active_sensors:
            highest_color = "blue"
        elif "green" in active_sensors:
            highest_color = "green"
        elif "white" in active_sensors:
            highest_color = "white"
    if highest_color != "":
        for s in sensors:
            if sensors[s]["color"] == highest_color:
                slm_status = "{}, {}".format(sensors[s]["color"], sensors[s]["status"])
    opcua_server.myvar.set_value(slm_status)

switcher = {"red":opcua_update_red, "green":opcua_update_green, 
            "yellow":opcua_update_yellow, "blue":opcua_update_blue, "white":opcua_update_white}



def run(my_mqtt_config_yaml):
    try:
        thread_opcua = threading.Thread(target=run_opcua)
        thread_opcua.start()
        mqtt = Mqtt(my_mqtt_config_yaml)
        lamp_status_before = ""
        status_changed = False
        while True:
            mqtt.start()
            previous_sensors = copy.deepcopy(sensors)
            check_for_blinking()
            update_sensors_status()
            for s in sensors:
                if sensors[s]["status"] is not previous_sensors[s]["status"]:
                    status_changed = True
            if status_changed:
                print("in if status_changed", end=" ", flush=True)
                status_changed = False
                update_mqtt_message()
                message_str = json.dumps(message)
                print("going to send", end=" ", flush=True)
                mqtt.publish(message_str)
                print("have sent", end=" ", flush=True)
            mqtt.disconnect()
    finally:
        #close connection, remove subcsriptions, etc
        opcua_server.server.stop()
        mqtt.disconnect()

def main():
    # the yml config file is passed through from the service file which is calling
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)


if __name__ == "__main__":
    main()