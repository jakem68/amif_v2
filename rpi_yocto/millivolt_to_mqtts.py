#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys, yocto_mV_rx
from my_mqtt_module import Mqtt

def run(tb_demo_yaml, mosquitto_yaml):
    mqtt_tb_demo = Mqtt(tb_demo_yaml)
    sensor_snr = mqtt_tb_demo.get_sensor_snr()
    time_interval = mqtt_tb_demo.get_time_interval()
    mqtt_tb_demo.start()
    mqtt_mosquitto = Mqtt(mosquitto_yaml)
    sensor_snr = mqtt_mosquitto.get_sensor_snr()
    time_interval = mqtt_mosquitto.get_time_interval()
    mqtt_mosquitto.start()
    yocto_mV_rx.initialize(sensor_snr)
    while True:
        datapoint = yocto_mV_rx.get_millivolts()
        msg = {"milliVolt":datapoint}
        msg_out = json.dumps(msg)
        mqtt_tb_demo.publish(msg_out = msg_out)
        mqtt_mosquitto.publish(msg_out = msg_out)
        time.sleep(time_interval)
        
def main():
    tb_demo_yaml = sys.argv[1]
    mosquito_yaml = sys.argv[2]
    run(tb_demo_yaml, mosquito_yaml)

if __name__ == "__main__":
    main()
