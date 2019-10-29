#!/home/jan/paho_mqtt_client/venv/bin/python3

import paho.mqtt.client as mqtt
import time, math, threading, json, socket_server

broker_url = "pc00392"
broker_port = 1883

flag_connected = 0
topic = "sirris/diep2/shop/polishing/cobot/status_changed"
time_interval = 0.25

def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1
    print("Connected With Result Code {}".format(rc))

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("Client Got Disconnected")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect

print("connecting")
client.connect(broker_url, broker_port, 60)
client.loop_start()

while not flag_connected == 1:
    print("waiting for connection to establish")
    time.sleep(0.5)

def create_mqtt_payload(msg):
    msg = msg.rstrip()
    if msg == 'START':
        mqtt_payload = {"status_iiwa":"busy"}
    elif msg == 'STOP':
        mqtt_payload = {"status_iiwa":"ready"}
    else:
        mqtt_payload = {"status_iiwa":"received unknown message from iiwa"}
    mqtt_payload_str = json.dumps(mqtt_payload)
    return mqtt_payload_str


def run():
    global flag_connected
    thread_sock = threading.Thread(target=socket_server.run)
    thread_sock.start()
    # socket_server.run()
    while True:
        if flag_connected == 1:
            if socket_server.msg_in_str != "" :
                mqtt_payload = create_mqtt_payload(socket_server.msg_in_str)
                client.publish(topic=topic, payload=mqtt_payload, qos=1, retain=False)
                socket_server.msg_in_str = ""
                print(mqtt_payload)
            # else:
            #     print("nothing to report")
        else:
            print("connection interrupted, waiting to reconnect")
        # time.sleep(time_interval)

def main():
    run()

if __name__ == "__main__":
    main()
