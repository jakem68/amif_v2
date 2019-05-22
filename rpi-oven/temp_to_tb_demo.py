#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics
from poweroff_dweet import dweet_run
from my_mqtt_module import Mqtt
from thermocouple_aio import sensor

# start dweet services
dweet_run("sirris.amifv2.oven")
time.sleep(5)
mqtt_demo = Mqtt("/home/pi/programs/my_mqtt_module.yml")
mqtt_demo.start()

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
        # check for stable reading by comparing two readings
        else:
            first_reading = sensor.readTempC()
            second_reading = sensor.readTempC()
        # check whether both readings are numbers
        if (isNaN(first_reading)) or (isNaN(second_reading)):
            print("temperature value is NaN")
            pass 
        else:
            if abs(first_reading - second_reading) > 2:
                print("temperature reading is not stable")
                print("first_reading is {}, and second_reading is {}".format(first_reading, second_reading))
                pass
            # check whether new reading makes sense by comparing with last ten readings
            # within range of +/- 3*stdev of last ten readings. If outside this range don't send to TB for now but 
            #  add it to the list of last ten readings --> increases stdev for evaluation of next reading
            else:
                temp = first_reading
                if len(last_ten_temps) < 10:
                    last_ten_temps = [temp]*10

                if temp_is_valid(temp, last_ten_temps):
                    msg = {"temperature": temp}
                    msg_out = json.dumps(msg)
                    mqtt_demo.publish(msg_out = msg_out)
                else:
                    print("last reading was an outlier")
            last_ten_temps.insert(0, temp)
            last_ten_temps.pop(10)
        time.sleep(mqtt_demo.get_time_interval())
        
def main():
    run()

if __name__ == "__main__":
    main()
