#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys
from my_mqtt_module import Mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855


### TODO: write function around this and repeat for other thermocouples to be able to switch between sensors easily
# Configuration of Raspberry Pi software SPI.
CLK = 25
CS  = 24
DO  = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)


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

def run(my_mqtt_config_yaml):
    mqtt = Mqtt(my_mqtt_config_yaml)
    mqtt.start()

    last_ten_temps = []
    while True:
        # check for stable reading by comparing two readings
        first_reading = sensor.readTempC()
        second_reading = sensor.readTempC()
        # check whether both readings are numbers
        if (isNaN(first_reading)) or (isNaN(second_reading)):
            print("temperature value is NaN")
            pass 
        else:
            # avoid outliers when 3*stdev is wide by evaluating 2 immediate consecutive measurements
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
                    mqtt.publish(msg_out = msg_out)
                else:
                    print("last reading was an outlier")
            last_ten_temps.insert(0, temp)
            last_ten_temps.pop(10)
        time.sleep(mqtt.get_time_interval())
        
def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)

if __name__ == "__main__":
    main()
