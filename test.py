#!/usr/bin/env python
# pylint: disable=invalid-name, line-too-long, unused-import
"""Test Sardana."""

import time
import sys

import PyTango
from sardana.taurus.core.tango.sardana.macroserver import BaseDoor, BaseMacroServer

def is_door(door_name):
    db = PyTango.Database()
    server_list = db.get_server_list('MacroServer/*').value_string
    for server in server_list:
        server_devs = db.get_device_class_list(server).value_string
        devs, classes = server_devs[0::2], server_devs[1::2]
        for idx, dev in enumerate(devs):
            if dev.lower() == door_name.lower():
                if classes[idx] == "Door":
                    return True
                else:
                    return False
    return False

DOOR_NAME = "cfeld/door/cfeld-pcx27083.01"
if not is_door(DOOR_NAME):
    print "not door"
    sys.exit(1)
db = PyTango.Database()
door_full_name = "%s:%s/%s" % (db.get_db_host(), db.get_db_port(), DOOR_NAME)
door = BaseDoor(door_full_name)
output = door.getLogObj('output')
debug = door.getLogObj('debug')

output.clearLogBuffer()
debug.clearLogBuffer()
# door.runmacro(["wa"])
# door.runmacro(["mv", "exp_dmy01", "0"])
door.runmacro(["ascan", "exp_dmy01", "0", "1", "10", "0.2"])
while not debug.getLogBuffer():
    print "empty"
    time.sleep(0.05)
while door.getState() != PyTango.DevState.ON:
    print "running"
    time.sleep(0.05)
print output.getLogBuffer()
print debug.getLogBuffer()
