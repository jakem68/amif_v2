#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys, yocto_mV_rx, yocto_mA_tx
from my_mqtt_module import Mqtt

def get_new_current_set_value(current_set_value=2, climbing=True):
    max_mA = 6
    min_mA = 4.5
    increment = 0.5
    if climbing and current_set_value < max_mA:
        current_set_value += increment
    if not climbing and current_set_value > min_mA:
        current_set_value -= increment
    if current_set_value == max_mA:
        climbing = False
    if current_set_value == min_mA:
        climbing = True
    current_set_value = 4.5
    return current_set_value, climbing


def run(tb_demo_yaml, mosquitto_yaml):
    mqtt_tb_demo = Mqtt(tb_demo_yaml)
    mqtt_tb_demo.start()
    mqtt_mosquitto = Mqtt(mosquitto_yaml)
    mqtt_mosquitto.start()
    sensor_snr_mV = mqtt_mosquitto.get_yml_item("sensor_snr_mV")
    sensor_snr_mA = mqtt_mosquitto.get_yml_item("sensor_snr_mA")
    # current_set_value = mqtt_mosquitto.get_yml_item("current_set_value")
    current_set_value = get_new_current_set_value()
    time_interval = mqtt_mosquitto.get_time_interval()
    yocto_mV_rx.initialize(sensor_snr_mV)
    loop = yocto_mA_tx.initialize(sensor_snr_mA)
    while True:
        yocto_mA_tx.set_current(current_set_value[0], loop)
        milliamp = float(loop.get_advertisedValue())
        time.sleep(0.25)
        millivolt = yocto_mV_rx.get_millivolts()
        ohm = round(millivolt/milliamp, 2)
        temperature = (ohm*5.3739)-972
        msg = {"milliVolt":millivolt, "milliamp":milliamp, "ohm":ohm, "temperature":temperature}
        msg_out = json.dumps(msg)
        mqtt_tb_demo.publish(msg_out = msg_out)
        mqtt_mosquitto.publish(msg_out = msg_out)
        current_set_value = get_new_current_set_value(current_set_value[0], current_set_value[1])
        time.sleep(time_interval)
        
def main():
    tb_demo_yaml = sys.argv[1]
    mosquito_yaml = sys.argv[2]
    run(tb_demo_yaml, mosquito_yaml)

if __name__ == "__main__":
    main()
