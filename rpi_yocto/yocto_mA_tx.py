#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

from yoctopuce.yocto_api import *
from yoctopuce.yocto_currentloopoutput import *


def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number> value')
    print(scriptname + ' <logical_name> value')
    print(scriptname + ' any value ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')

def initialize(target="any"):
    errmsg = YRefParam()
    # Setup the API to use local USB devices
    if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
        sys.exit("init error" + errmsg.value)

    if target == 'any':
        # retreive any currentLoopOutput
        loop = YCurrentLoopOutput.FirstCurrentLoopOutput()
        if loop is None:
            die('No module connected')
    else:
        loop = YCurrentLoopOutput.FindCurrentLoopOutput(target + '.currentLoopOutput')

    # we need to retreive the second loop from the device
    if not loop.isOnline(): die('device not connected')

def set_current(value):
    loop.set_current(value)

    loopPower = loop.get_loopPower()

    if loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
        print("Current loop not powered")
    elif loopPower == YCurrentLoopOutput.LOOPPOWER_NOPWR:
        print("Insufficient voltage on current loop")
    else:
        sys.exit("current loop set to " + str(value) + " mA")
    YAPI.FreeAPI()


def main():
    if len(sys.argv) < 3:
        usage()

    target = sys.argv[1]
    value = float(sys.argv[2])

if __name__ == "__main__":
    main()

