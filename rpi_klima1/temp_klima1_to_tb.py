#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics
from my_mqtt_module import mqtt_publish, time_interval
from read_ds18b20_temp import get_temperature

sensor_snr = "28-051692d95eff" # sensor snr for klima1 (= Fehlmann room)

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

def run():
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
                msg = {"temperature": temp}
                msg_out = json.dumps(msg)
                mqtt_publish(msg_out = msg_out)
            else:
                print("last reading was an outlier")
            last_ten_temps.insert(0, temp)
            last_ten_temps.pop(10)
        time.sleep(time_interval)
        
def main():
    run()

if __name__ == "__main__":
    main()
