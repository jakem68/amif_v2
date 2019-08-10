#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys
from my_mqtt_module import Mqtt
from read_ds18b20_temp import get_temperature


def isNaN(num):
    return num != num

# checks whether new value is within + or - 3*stdev of last 10 values
def temp_is_valid(temp, last_ten_temps):
    try:
        mean = statistics.mean(last_ten_temps)
        stdev = statistics.stdev(last_ten_temps)
        print("{}, stdev is {}, mean is {}".format(last_ten_temps, stdev, mean))
    except:
        print("some error")
    if (temp > mean + (3*stdev)) or (temp < mean - (3*stdev)):
        result = False
    else:
        result = True
    return result    

def run(my_mqtt_config_yaml):
    mqtt = Mqtt(my_mqtt_config_yaml)
    mqtt.start()
    sensor_snr = mqtt.get_sensor_snr()
    time_interval = mqtt.get_time_interval()
    last_ten_temps = []
    while True:
        datapoint = get_temperature(sensor_snr)
        if isNaN(datapoint):
            print("temperature value is NaN")
            pass 
        else:
            temp = datapoint
            if len(last_ten_temps) < 10:
                last_ten_temps = [temp]*10

            if temp_is_valid(temp, last_ten_temps):
                mqtt.publish(msg_out = temp)
            else:
                print("last reading was an outlier")
            last_ten_temps.insert(0, temp)
            last_ten_temps.pop(10)
        time.sleep(time_interval)
        
def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)

if __name__ == "__main__":
    main()
