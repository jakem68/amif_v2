#!/home/jan/paho_mqtt_client/venv/bin/python3

import paho.mqtt.client as mqtt
import time, json, socket
from influxdb_ksj import write_points

# broker_url = "iot.eclipse.org"
#broker_url = "test.mosquitto.org"
# broker_url = "broker.hivemq.com"
broker_url = "172.16.10.1"
broker_port = 1883

flag_connected = 0
messages_to_be_handled = []
# topic_listen = "ksj_value1"
topic_listen = "sirris/#"
topic_send = "ksj_value2"
my_hostname = socket.gethostname()

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
    messages_to_be_handled.append(message)

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

def handle_rfid(msg):
    location = msg.topic
    status = json.loads(msg.payload.decode())['payload'].split(",")[4]
    rfid_tag = "".join(json.loads(msg.payload.decode())['payload'].split(",")[:4])
    if status == "ON":
        status = 1
    elif status == "OFF":
        status = 0
    else:
        status = -1
    json_body = [
        {
            "measurement": "rfid_events",
            "tags": {
                "mqtt_consumer_agent": my_hostname,
                "rfid_tag": rfid_tag,
                "topic": msg.topic
            },
            "time": int(round(time.time()*1000000000)),
            "fields": {
                "status": status
            }
        }
    ]

    print(json_body)

    if write_points(json_body):
        print("succes")
    else:
        print("no influx")




def run():
    global flag_connected
    global messages_to_be_handled
    print (len(messages_to_be_handled))
    while True:
        if flag_connected == 1:
            if len(messages_to_be_handled) > 0: 
                msg = messages_to_be_handled[0]
                # client.publish(topic=topic_send, payload="handled message {}".format(messages_to_be_handled[0]), qos=1, retain=False)
                # print("handled message {}".format(msg.payload.decode()))
                if "rfid" in msg.topic:
                    handle_rfid(msg)
                messages_to_be_handled.pop(0)


        else:
            print("connection interrupted, waiting to reconnect")
        time.sleep(0.5)

def main():
    run()

if __name__ == "__main__":
    main()