#!/home/jan/paho_mqtt_client/venv/bin/python3

import paho.mqtt.client as mqtt
import time, math

# broker_url = "iot.eclipse.org"
#broker_url = "test.mosquitto.org"
broker_url = "broker.hivemq.com"
broker_port = 1883

flag_connected = 0
topic = "ksj_value1"
time_interval_mqtt_send = 0.1

x_axis_steps = 5
sine_amplitude = 100
sine_displacement = 0

def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("Client Got Disconnected")

def calculate_sine_datapoint(x_value):
        sine_datapoint = int(round(math.sin(math.radians(x_value))
                               *sine_amplitude))+sine_displacement
        return sine_datapoint

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

print("connecting")
client.connect(broker_url, broker_port, 60)
client.loop_start()

while not flag_connected == 1:
    print("waiting for connection to establish")
    time.sleep(0.5)


def run():
    global flag_connected
    x_value=0
#    while True:
    for i in range(50):
        if flag_connected == 1:
            datapoint = calculate_sine_datapoint(x_value)
            x_value += x_axis_steps
#            client.publish(topic=topic, payload=datapoint, qos=1, retain=False)
            client.publish(topic=topic, payload=i, qos=1, retain=False)
#            print(datapoint)
            print(i)
            time.sleep(time_interval_mqtt_send)
        else:
            print("connection interrupted, waiting to reconnect")
            time.sleep(0.5)

def main():
    run()

if __name__ == "__main__":
    main()