#!/home/jan/paho_mqtt_client/venv/bin/python3

import paho.mqtt.client as mqtt
import os, time, socket, json

# broker_url = "iot.eclipse.org"
#broker_url = "test.mosquitto.org"
# broker_url = "broker.hivemq.com"
broker_url = "172.16.10.1"
broker_port = 1883

flag_connected = 0
# topic_listen = "ksj_value1"
topic_send = "sirris/diep2/system"
influxdb_directory = "/var/lib/influxdb"
my_hostname = socket.gethostname()


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

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def run():
    global flag_connected
    while True:
        if flag_connected == 1:
            # client.publish(topic=topic_send, payload="handled message {}".format(messages_to_be_handled[0]), qos=1, retain=False)
            # print("handled message {}".format(msg.payload.decode()))
            value = get_size(influxdb_directory)
            print(value, 'bytes')
            key = "influxdb size"
            msg = {key : value, "host" : my_hostname}
            msg = json.dumps(msg)
            client.publish(topic=topic_send, payload=msg)
            time.sleep(600)
        else:
        # Wait to reconnect
            while not flag_connected == 1:
                try:
                    print("disconnected, trying to reconnect.")
                    client.connect(broker_url,broker_port,60)
                    time.sleep(0.5)
                    client.loop()
                except:
                    time.sleep(1)
                    pass
            
        time.sleep(0.5)

def main():
    run()

if __name__ == "__main__":
    main()