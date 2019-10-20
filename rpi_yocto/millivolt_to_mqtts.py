#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys, yocto_mV_rx, yocto_mA_tx
from my_mqtt_module import Mqtt

def run(tb_demo_yaml, mosquitto_yaml):
    mqtt_tb_demo = Mqtt(tb_demo_yaml)
    mqtt_tb_demo.start()
    mqtt_mosquitto = Mqtt(mosquitto_yaml)
    mqtt_mosquitto.start()
    sensor_snr_mV = mqtt_mosquitto.get_yml_item("sensor_snr_mV")
    sensor_snr_mA = mqtt_mosquitto.get_yml_item("sensor_snr_mA")
    current_set_value = mqtt_mosquitto.get_yml_item("current_set_value")
    time_interval = mqtt_mosquitto.get_time_interval()
    yocto_mV_rx.initialize(sensor_snr_mV)
    yocto_mA_tx.initialize(sensor_snr_mA)
    yocto_mA_tx.set_current(current_set_value)
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
