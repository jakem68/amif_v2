#!/home/jan/paho_mqtt_client/venv/bin/python3

import paho.mqtt.client as mqtt
import time

# broker_url = "iot.eclipse.org"
#broker_url = "test.mosquitto.org"
broker_url = "172.16.10.1"
broker_port = 1883

flag_connected = 0
messages_to_be_handled = []
topic_listen = "sirris/diep2/klima1/apex/machine/command"
topic_send = "sirris/diep2/klima1/apex/machine/status_changed"

def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("Client Got Disconnected")

def on_message(client, userdata, message):
    global messages_to_be_handled
    # print("Message Received: "+message.payload.decode())
    messages_to_be_handled.append(message.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("connecting")
client.connect(broker_url, broker_port, 60)
client.subscribe(topic_listen)
client.loop_start()

while not flag_connected == 1:
    print("waiting for connection to establish")
    time.sleep(0.5)

def get_most_recent_message():
    global messages_to_be_handled
    most_recent_message = ""
    if messages_to_be_handled:
        most_recent_message = messages_to_be_handled[-1]
    messages_to_be_handled = []
    return most_recent_message

def publish(payload):
    client.publish(topic=topic_send, payload=payload)

def run():
    global flag_connected
    global messages_to_be_handled
    print (len(messages_to_be_handled))
    while True:
        if flag_connected == 1:
            if len(messages_to_be_handled) > 0: 
                client.publish(topic=topic_send, payload="handled message {}".format(messages_to_be_handled[0]), qos=1, retain=False)
                print("handled message {}".format(messages_to_be_handled[0]))
                messages_to_be_handled.pop(0)
                time.sleep(1)
            else:
                print("connection ok, waiting for message")
                time.sleep(1)
        else:
            print("connection interrupted, waiting to reconnect")
            time.sleep(0.5)

def main():
    run()

if __name__ == "__main__":
    main()
