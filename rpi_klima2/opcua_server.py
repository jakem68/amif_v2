#!/usr/bin/python3

__author__ = 'Jan Kempeneers'

import datetime, time, math, json, statistics, sys
from read_ds18b20_temp import get_temperature

sensor_snr = "28-03168af0c4ff" # sensor snr for klima2 (= Lasea room)
time_interval = 1


# initialize and start server (in function or not?)
sys.path.insert(0, "..")
from opcua import ua, Server

# setup our server
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/sirris/server/")

# setup our own namespace, not really necessary but should as spec
uri = "http://examples.sirris.github.io"
idx = server.register_namespace(uri)

# get Objects node, this is where we should put our nodes
objects = server.get_objects_node()

# populating our address space
myobj = objects.add_object(idx, "AMIF_klima2_temp")
myvar = myobj.add_variable(idx, "klima2_temp", 6.7)
myvar.set_writable()    # Set MyVariable to be writable by clients

server.start()

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
    try: 
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
                    myvar.set_value(temp)
                else:
                    print("last reading was an outlier")
                last_ten_temps.insert(0, temp)
                last_ten_temps.pop(10)
            time.sleep(time_interval)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()
        
def main():
    run()

if __name__ == "__main__":
    main()
