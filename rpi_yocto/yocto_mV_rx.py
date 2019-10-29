# ********************************************************************
#
#  $Id: helloworld.py 32630 2018-10-10 14:11:07Z seb $
#
#  An example that show how to use a  Yocto-milliVolt-Rx
#
#  You can find more information on our web site:
#   Yocto-milliVolt-Rx documentation:
#      https://www.yoctopuce.com/EN/products/yocto-millivolt-rx/doc.html
#   Python API Reference:
#      https://www.yoctopuce.com/EN/doc/reference/yoctolib-python-EN.html
#
# *********************************************************************

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yoctopuce.yocto_api import *
from yoctopuce.yocto_genericsensor import *

channel1 = ""

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()

def die(msg):
    sys.exit(msg + ' (check USB cable)')

def measure_continuously():
    global channel1
    while channel1.isOnline():
        print("Voltage:  %f %s" % (channel1.get_currentValue(), channel1.get_unit()))
        print("  (Ctrl-C to stop)")
        YAPI.Sleep(1000)
    YAPI.FreeAPI()

def get_millivolts():
    global channel1
    return channel1.get_currentValue()

def initialize(target="any"):
    global channel1
    errmsg = YRefParam()

    # setup to use Virtualhub instead of native usb to work with multiple devices
    if YAPI.RegisterHub("127.0.0.1", errmsg) != YAPI.SUCCESS:
        print("no succes, trying via usb native")
        if (YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS):
            print(errmsg)

    if target == 'any':
        # retreive any genericSensor sensor
        sensor = YGenericSensor.FirstGenericSensor()
        if sensor is None:
            die('No module connected')
    else:
        sensor = YGenericSensor.FindGenericSensor(target + '.genericSensor1')

    if not (sensor.isOnline()):
        die('device not connected')

    # retreive module serial
    serial = sensor.get_module().get_serialNumber()
    print("Serial number of sensor is : " + serial)

    # retreive both channels
    channel1 = YGenericSensor.FindGenericSensor(serial + '.genericSensor1')

def main():
    try:
        target = sys.argv[1]
    except:
        target = "any"
        pass
    if len(sys.argv) < 2:
        usage()
    initialize(target)
    get_millivolts()
    measure_continuously()

if __name__ == "__main__":
    main()
