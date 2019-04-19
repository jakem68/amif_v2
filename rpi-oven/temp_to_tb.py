#!/home/jan/paho_mqtt_client/venv/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics
from my_mqtt_module import mqtt_publish, time_interval
from thermocouple_aio import sensor


sine_dataflow_enabled = False
x_axis_steps = 10
sine_amplitude = 100
sine_displacement = 100

def calculate_sine_datapoint(x_value):
        sine_datapoint = int(round(math.sin(math.radians(x_value))
                               *sine_amplitude))+sine_displacement
        return sine_datapoint

def isNaN(num):
    return num != num

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
    x_value=0
    while True:
        if sine_dataflow_enabled:
            datapoint = calculate_sine_datapoint(x_value)
            x_value += x_axis_steps
        else:
            datapoint = sensor.readTempC()
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
