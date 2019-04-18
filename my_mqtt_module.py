#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import paho.mqtt.client as mqtt
import time, math, json, yaml

# interpreting the yaml config file

with open("my_mqtt_module.yml", 'r') as f:
    try:
        cfg_dic = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)
server = cfg_dic["mqtt_publisher"]["server"]
port = cfg_dic["mqtt_publisher"]["port"]
#topic = "rpi-oven/temperature"
topic = cfg_dic["mqtt_publisher"]["topic"]
username = cfg_dic["mqtt_publisher"]["username"]
password = cfg_dic["mqtt_publisher"]["password"]
time_interval = cfg_dic["mqtt_publisher"]["time_interval"]

sine_dataflow_enabled = cfg_dic["sine_dataflow"]["enable"]
x_axis_steps = cfg_dic["sine_dataflow"]["x_axis_steps"]
sine_amplitude = cfg_dic["sine_dataflow"]["sine_amplitude"]
sine_displacement = cfg_dic["sine_dataflow"]["sine_displacement"]

# This is the Publisher

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print("connected to mqtt broker")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

def initialize_mqtt_client(server=server, port=port, username=username, password=password):
    if username != "":
        client.username_pw_set(username, password)

    client.connect(server,port,60)

    while not flag_connected == 1:
        client.loop()

    print("mqtt client connected")

def publish_mqtt_message(topic, msg_out):
    if flag_connected == 1:
    # Publish message
        client.publish(topic, msg_out)
        print(msg_out)
    else:
    # Wait to reconnect
        client.connect(server,port,60)
#       client.loop_forever()

def calculate_sine_datapoint(x_value):
        sine_datapoint = int(round(math.sin(math.radians(x_value))*sine_amplitude))+sine_displacement
        return sine_datapoint


def run():
    initialize_mqtt_client()
    x_value=0
    while True:
        if sine_dataflow_enabled == True:
            sine_datapoint = calculate_sine_datapoint(x_value)
            msg = {"temperature": sine_datapoint}
        else:
            msg = None
        msg_out = json.dumps(msg)
        publish_mqtt_message(topic, msg_out)
        time.sleep(1)
        x_value += x_axis_steps
    client.disconnect()

def main():
    run()

if __name__ == "__main__":
    main()