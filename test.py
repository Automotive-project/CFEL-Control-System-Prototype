#!/usr/bin/python
"""Test Tango"""

import time

import PyTango

# pylint: disable=C0103


###########
#  Motor  #
###########
dummy_motor = PyTango.DeviceProxy("exp_dmy01")
print dummy_motor.position

############
#  Camera  #
############
# Ref1: http://lima.blissgarden.org/camera/pointgrey/doc/index.html
# Ref2: http://lima.blissgarden.org/applications/tango/doc/index.html
NUM_FRAMES = 1

camera1 = PyTango.DeviceProxy("cfeld/limaccds/poingrey")
camera1.acq_nb_frames = NUM_FRAMES
camera1.acq_expo_time = 1.0
camera1.prepareAcq()
camera1.startAcq()
# Wait until all images are captured.
while camera1.last_image_ready != NUM_FRAMES - 1:
    print camera1.last_image_ready + 1
    time.sleep(.1)
# Read the first image in DATA_ARRAY format.
image = camera1.readImage(0)
# Write the first image to file in RAW format.
camera1.saving_directory = "/home/ax01user/test/"
camera1.saving_prefix = "PG"
camera1.saving_suffix = "raw"
# TODO: try other formats (edf, edfgz, cbf)
camera1.saving_format = "RAW"
camera1.saving_overwrite_policy = "OVERWRITE"
camera1.writeImage(0)
