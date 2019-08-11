#! /usr/bin/python3

import time, sys, json, copy

sensors = {
    "sensor1": {
        "color": "white",
        "pin": 3,
        "value": False,
        "status": "off",
        "changes": 0,
        },
    "sensor2": {
        "color": "red",
        "pin": 4,
        "value": False,
        "status": "off",
        "changes": 0,
        },
    "sensor3": {
        "color": "yellow",
        "pin": 17,
        "value": False,
        "status": "off",
        "changes": 0,
        },
    "sensor4": {
        "color": "blue",
        "pin": 22,
        "value": False,
        "status": "off",
        "changes": 0,
        },
    "sensor5": {
        "color": "green",
        "pin": 27,
        "value": False,
        "status": "off",
        "changes": 0,
        },
    }


def toggle_value(color):
    for s in sensors:
        if sensors[s]["color"] == color:
            sensors[s]["value"] = not sensors[s]["value"]

# def print_color_statusses(sensor_dict, name):
#     for s in sensor_dict:
#         print("{} {} is {}".format(name, sensor_dict[s].get("color"), sensor_dict[s].get("value")))

def return_changed_colors(sensor_dict_one, sensor_dict_two):
    changed_colors = []
    for s in sensor_dict_one:
        if sensor_dict_one[s]["value"] != sensor_dict_two[s]["value"]:
            changed_colors.append(sensor_dict_one[s]["color"])
    return changed_colors

def opcua_update_green():
    print("green")

def opcua_update_red():
    print("red")

def opcua_update_yellow():
    print("yellow")

def opcua_update_blue():
    print("blue")

def opcua_update_white():
    print("white")

previous_sensors = copy.deepcopy(sensors)
switcher = {"red":opcua_update_red, "green":opcua_update_green, 
            "yellow":opcua_update_yellow, "blue":opcua_update_blue, "white":opcua_update_white}

for i in range(2):
    changed_colors = return_changed_colors(sensors, previous_sensors)
    toggle_value("green")
    toggle_value("red")
    for i in changed_colors:
        switcher.get(i)()


# def update_sensor_values():
#     # read sensor values: looping through sensors and get inversed GPIO pin value
#     for s in sensors:
#         sensors[s]["value"] = str(not GPIO.input(sensors[s]["pin"]))
#         # reset detected changes to zero
#         sensors[s]["changes"] = 0

# def update_opcua_variables():
#     for s in sensors:
#         color = sensors[s]["color"]
#         value = sensors[s]["value"]
#         status = sensors[s]["status"]

# def green(value, status):
#     opcua_server.green_value.set_value(value)
#     opcua_server.green_status.set_value(status)
