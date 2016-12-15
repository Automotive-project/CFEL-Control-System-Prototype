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
camera1 = PyTango.DeviceProxy("cfeld/limaccds/poingrey")

NUM_FRAMES = 1
MIN_EXPO_TIME = camera1.valid_ranges[0]
MAX_EXPO_TIME = camera1.valid_ranges[1]
EXPO_TIME = 0.1
FILE_INDEX = 4

camera1.acq_nb_frames = NUM_FRAMES
camera1.acq_expo_time = EXPO_TIME
camera1.prepareAcq()
camera1.startAcq()
# Wait until all images are captured.
while camera1.last_image_ready != NUM_FRAMES - 1:
    print camera1.last_image_ready + 1
    time.sleep(.1)
# Read the first image in DATA_ARRAY format.
# image = camera1.readImage(0)
# Write the first image to file in RAW format.
camera1.saving_directory = "/home/ax01user/test/"
camera1.saving_prefix = "PG"
camera1.saving_next_number = FILE_INDEX
camera1.saving_suffix = "raw"
# Todo: try other formats (edf, edfgz, cbf)
camera1.saving_format = "RAW"
camera1.saving_overwrite_policy = "OVERWRITE"
camera1.writeImage(0)
