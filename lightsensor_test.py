#! /usr/bin/python3

import RPi.GPIO as GPIO
import time, sys
from Adafruit_IO import MQTTClient

GPIO.setmode(GPIO.BCM)

sensors_on_pin = {"sensor1": 3}

# loop through pins to set them as DIG IN
for s in sensors_on_pin:
    GPIO.setup(sensors_on_pin[s],GPIO.IN)


ADAFRUIT_IO_KEY = '0642323bbbf34022955dd1f38024dfce'

ADAFRUIT_IO_USERNAME = 'jankempeneers'

feed_name = "lamp_status"
feed_id = "sirris10-amifv2.lamp-status"


# callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {feed_name} changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(feed_name)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined below.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()


def main():
    while True:
        sensor_values = {}

        # read sensor values
        for s in sensors_on_pin:
            sensor_values[s] = not GPIO.input(sensors_on_pin[s])
        print(sensor_values)
#        client.publish(feed_id, str(sensor_values))
        client.publish(feed_id, str(sensor_values["sensor1"]))
        time.sleep(2)
	

if __name__ == "__main__":
    main()
