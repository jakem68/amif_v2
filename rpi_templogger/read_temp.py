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

def get_temp_reading(sensor):
    temps = []
    for count in range(5):
        temps.append(sensor["max31855"].readTempC())
        time.sleep(0.05)
    if temps == [] or statistics.stdev(temps) > 1:
        temp_final = ""
    else:
        for index, temp in enumerate(temps):
            if isNaN(temp):
                temps.pop(index)
        if not temps == []:
            for temp in temps:
                if abs(temp - statistics.mean(temps)) > 3 * statistics.stdev(temps):
                    temps.pop(index)
            if not temps == []:
                temp_final = statistics.mean(temps)
            else:
                temp_final = ""
        else:
            temp_final = ""
    return temp_final

def temp_is_valid(temp, last_ten_temps, max_delta_temp_per_interval):
    try:
        mean = statistics.mean(last_ten_temps)
        stdev = statistics.stdev(last_ten_temps)
        if stdev < max_delta_temp_per_interval:
            stdev = max_delta_temp_per_interval
        print("{}, stdev is {}, mean is {}".format(last_ten_temps, stdev, mean))
    except:
        print("some error")
    if (temp > mean + (3*stdev)) or (temp < mean - (3*stdev)):
        result = False
    else:
        result = True
    return result

def reconnect_mqtt(mqtt):
    mqtt.disconnect()
    mqtt.start()

def run(my_mqtt_config_yaml):
    mqtt = Mqtt(my_mqtt_config_yaml)
    time_interval = mqtt.get_time_interval()
    max_delta_temp_per_sec = 0.1
    max_delta_temp_per_interval = time_interval*max_delta_temp_per_sec
    mqtt_reconnect_counter = 0
    while True:
        if mqtt_reconnect_counter == 10:
            reconnect_mqtt(mqtt)
        for sensor in sensors.values():
            # check for stable reading by comparing two readings
            temp = get_temp_reading(sensor)
            last_ten_temps = sensor["last_ten_temps"]
            # check whether new reading makes sense by comparing with last ten readings
            # within range of +/- 3*stdev of last ten readings. If outside this range don't send to TB for now but
            #  add it to the list of last ten readings --> increases stdev for evaluation of next reading
            if len(last_ten_temps) < 10:
                last_ten_temps = [temp]*10
            if temp_is_valid(temp, last_ten_temps, max_delta_temp_per_interval):
                sensor["temp"] = temp
            else:
                print("last reading was an outlier")
            last_ten_temps.insert(0, temp)
            last_ten_temps.pop(10)
            sensor["last_ten_temps"] = last_ten_temps

        msg = {}
        for sensor in sensors:
            key = sensor + "_temp"
            value = sensors[sensor]["temp"]
            if isNaN(value):
                value = ""
            msg.update({key : value})
        msg_out = json.dumps(msg)
        mqtt.publish(msg_out = msg_out)
        mqtt_reconnect_counter += 1
        time.sleep(time_interval)


def main():
    my_mqtt_config_yaml = sys.argv[1]
    run(my_mqtt_config_yaml)

if __name__ == "__main__":
    main()
