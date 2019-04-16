#!python3

__author__ = 'Jan Kempeneers'

import paho.mqtt.client as mqtt
import time, math, json

# This is the Publisher

server = "127.0.0.1"
port = 1883
#topic = "rpi-oven/temperature"
topic = "v1/devices/me/telemetry"
username = "IrEKQCfL5fS1v5sJ1QWo"
password = ""

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
        sine_datapoint = int(round(math.sin(math.radians(x_value))*100))+100
        return sine_datapoint


def run():
    initialize_mqtt_client()
    x_value=0
    while True:
        # values = {'switch1': switch1}
        sine_datapoint = calculate_sine_datapoint(x_value)
        msg = {"temperature": sine_datapoint}
        msg_out = json.dumps(msg)
        publish_mqtt_message(topic, msg_out)
        time.sleep(1)
        x_value += 10
    client.disconnect()

def main():
    run()

if __name__ == "__main__":
    main()