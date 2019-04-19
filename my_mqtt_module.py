#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import paho.mqtt.client as mqtt
import time, json, yaml

# interpreting the yaml config file

with open("my_mqtt_module.yml", 'r') as f: # use full path to file
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

# This is the Publisher

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1
   print("connected to mqtt broker")

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

def client_initialize(server=server, port=port, username=username, password=password):
    if username != "":
        client.username_pw_set(username, password)

    client.connect(server,port,60)

    while not flag_connected == 1:
        client.loop()

    print("mqtt client connected")

def mqtt_publish(msg_out, topic=topic):
    if flag_connected == 1:
    # Publish message
        client.publish(topic, msg_out)
        print(msg_out)
    else:
    # Wait to reconnect
        client.connect(server,port,60)
#       client.loop_forever()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client_initialize()

# sending some values for when testing

def run():
    value=0
    while True:
        msg = {"temperature": value}
        msg_out = json.dumps(msg)
        mqtt_publish(msg_out)
        time.sleep(1)
        value += 1
    client.disconnect()

def main():
    run()

if __name__ == "__main__":
    main()
