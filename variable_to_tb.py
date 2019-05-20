#!/home/jan/paho_mqtt_client/venv/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json
from my_mqtt_module import Mqtt

mqtt1 = Mqtt("my_mqtt_module.yml")
mqtt1.start()

sine_dataflow_enabled = True
x_axis_steps = 10
sine_amplitude = 100
sine_displacement = 100

def calculate_sine_datapoint(x_value):
        sine_datapoint = int(round(math.sin(math.radians(x_value))
                               *sine_amplitude))+sine_displacement
        return sine_datapoint


def run():
    x_value=0
    while True:
        if sine_dataflow_enabled:
            datapoint = calculate_sine_datapoint(x_value)
            x_value += x_axis_steps
        else:
            datapoint = x_value
            x_value += 10
        msg = {"temperature": datapoint}
        msg_out = json.dumps(msg)
        mqtt1.publish(msg_out = msg_out)
        time.sleep(1)
    mqtt1.client.disconnect()
        
def main():
    run()

if __name__ == "__main__":
    main()