#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys, yocto_mV_rx
from my_mqtt_module import Mqtt

def run(my_mqtt_config_yaml):
    mqtt = Mqtt(my_mqtt_config_yaml)
    sensor_snr = mqtt.get_sensor_snr()
    time_interval = mqtt.get_time_interval()
    mqtt.start()
    yocto_mV_rx.initialize(sensor_snr)
    while True:
        datapoint = yocto_mV_rx.get_millivolts()
        msg = {"milliVolt":datapoint}
        msg_out = json.dumps(msg)
        mqtt.publish(msg_out = msg_out)
        time.sleep(time_interval)
        
def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)

if __name__ == "__main__":
    main()
