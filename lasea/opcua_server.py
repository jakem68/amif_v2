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

