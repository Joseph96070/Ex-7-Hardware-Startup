#
# This Script is for bare bones functionality testing of the RPiMIB
#
# This file is intended to be a script that is run from ipython3, for example the code here should be copied an pasted
# sometimes line by line into the ipython3 console.
#
# At some point this should be made into a full testing script that can be run from the command line.
# Or perhaps it can be brought into Unit Tests.

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()

# Init a 200 steps per revolution stepper on Port 0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)

s0.start_relative_move(5)  # make motor on port 0 rotate 5 turns

s0.free_all()

cyprus.initialize()  # initialize the cyprus
version = cyprus.read_firmware_version()  # read the version of the cyprus firmware
print(version)  # print the version to the screen - should be something like 3.1.2 (11/12/19)

cyprus.setup_servo(1)  # sets up P4 on the RPiMIB as a RC servo style output

cyprus.set_servo_position(1, 0)  # 1 specifies port P4, 0 is a float from 0-1 that specifies servo position ~(0-180deg)

sleep(1)  # wait one second for the servo to get there

cyprus.set_servo_position(1, .5)  # 1 specifies port P4, 0.5 specifies servo position ~(0-180deg) range of (0-1)

sleep(1)  # wait one second for the servo to get there... minimum here should be about sleep(0.05)

cyprus.set_servo_position(1, 1)  # 1 specifies port P4, 1 specifies servo position ~(0-180deg) range of (0-1)

# test the RPiMIB P6 reads - connect a limit switch or proximity sensor to P6 run the code below
while True:
    if (cyprus.read_gpio() & 0b0001):    # binary bitwise AND of the value returned from read.gpio()
        sleep(1)
        if (cyprus.read_gpio() & 0b0001): #  a little debounce logic
            print("GPIO on port P6 is HIGH")
    else:
        print("GPIO on port P6 is LOW")
        sleep(1)
#   opening and closing the switch or proximity sensor should get the print to toggle between HIGH and LOW

# test the RPiMIB P7 reads - connect a limit switch or proximity sensor to P7 run the code below
while True:
    if (cyprus.read_gpio() & 0b0010):    # binary bitwise AND of the value returned from read.gpio()
        sleep(1)
        if (cyprus.read_gpio() & 0b0010):
            print("GPIO on port P7 is HIGH")
    else:
        print("GPIO on port P7 is LOW")
        sleep(1)
#   opening and closing the switch or proximity sensor should get the print to toggle between HIGH and LOW

# test the RPiMIB P8 reads - connect a limit switch or proximity sensor to P8 run the code below
while True:
    if (cyprus.read_gpio() & 0b0100):    # binary bitwise AND of the value returned from read.gpio()
        sleep(1)
        if (cyprus.read_gpio() & 0b0100): #  a little debounce logic
            print("GPIO on port P8 is HIGH")
    else:
        print("GPIO on port P8 is LOW")
        sleep(1)
#   opening and closing the switch or proximity sensor should get the print to toggle between HIGH and LOW

# test the RPiMIB P9 reads - connect a limit switch or proximity sensor to P9 run the code below
while True:
    if (cyprus.read_gpio() & 0b1000):    # binary bitwise AND of the value returned from read.gpio()
        sleep(1)
        if (cyprus.read_gpio() & 0b1000):
            print("GPIO on port P9 is HIGH")
    else:
        print("GPIO on port P9 is LOW")
        sleep(1)
#   opening and closing the switch or proximity sensor should get the print to toggle between HIGH and LOW
# when done disconnect the RPiMIB communication

cyprus.close()
spi.close()
GPIO.cleanup()