#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import time, math, json, statistics, sys
from my_mqtt_module import Mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

# Configuration of Raspberry Pi software SPI.
sensors = {
    "sensor1": {
        "CLK" : 22,
        "CS" : 27,
        "DO" : 17,
        "max31855" : "",
        "last_ten_temps" : [],
        "temp" : ""
    },
    "sensor2": {
        "CLK" : 24,
        "CS" : 23,
        "DO" : 18,
        "max31855" : "",
        "last_ten_temps" : [],
        "temp" : ""
    },
    "sensor3": {
        "CLK" : 11,
        "CS" : 9,
        "DO" : 10,
        "last_ten_temps" : []
    },
    "sensor4": {
        "CLK" : 7,
        "CS" : 8,
        "DO" : 25,
        "last_ten_temps" : []
    },
}

for sensor in sensors.values():
    CLK = sensor["CLK"]
    CS = sensor["CS"]
    DO = sensor["DO"]
    sensor["max31855"] = MAX31855.MAX31855(CLK, CS, DO)
# sys.exit("wanted stop")


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

    while True:
        for sensor in sensors.values():
            # check for stable reading by comparing two readings
            first_reading = sensor["max31855"].readTempC()
            second_reading = sensor["max31855"].readTempC()
            last_ten_temps = sensor["last_ten_temps"]
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
                    sensor["temp"] = temp
                    if len(last_ten_temps) < 10:
                        last_ten_temps = [temp]*10

                    # if temp_is_valid(temp, last_ten_temps):
                    #     sensor["temp"] = temp
                    # else:
                    #     print("last reading was an outlier")

                    last_ten_temps.insert(0, temp)
                    last_ten_temps.pop(10)
                    sensor["last_ten_temps"] = last_ten_temps
        msg = {}
        for sensor in sensors:
            key = sensor + "_temp"
            value = sensors[sensor]["temp"]
            msg.update({key : value})
        msg_out = json.dumps(msg)
        mqtt.publish(msg_out = msg_out)

        time.sleep(mqtt.get_time_interval())


def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)

if __name__ == "__main__":
    main()
