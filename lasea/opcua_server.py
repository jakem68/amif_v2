#!/usr/bin/python3

import datetime, time
import sys
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
myobj = objects.add_object(idx, "AMIF_lasea_slm")
myvar = myobj.add_variable(idx, "lasea_stack_light_status", 6.7)
myvar.set_writable()    # Set MyVariable to be writable by clients
# q.put(myvar)

red = myobj.add_object(idx, "red")
red_value = red.add_variable(idx, "red_value", 6.7)
red_status = red.add_variable(idx, "red_status", 6.7)

yellow = myobj.add_object(idx, "yellow")
yellow_value = yellow.add_variable(idx, "yellow_value", 6.7)
yellow_status = yellow.add_variable(idx, "yellow_status", 6.7)

blue = myobj.add_object(idx, "blue")
blue_value = blue.add_variable(idx, "blue_value", 6.7)
blue_status = blue.add_variable(idx, "blue_status", 6.7)

green = myobj.add_object(idx, "green")
green_value = green.add_variable(idx, "green_value", 6.7)
green_status = green.add_variable(idx, "green_status", 6.7)

white = myobj.add_object(idx, "white")
white_value = white.add_variable(idx, "white_value", 6.7)
white_status = white.add_variable(idx, "white_status", 6.7)

