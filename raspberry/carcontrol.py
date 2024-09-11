from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers

GPG = gopigo3.GoPiGo3() # Create an instance of the GoPiGo3 class. GPG is GoPiGo3 object.

try:
    for i in range(0, 101):
        GPG.set_motor_power(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, i)
        time.sleep(0.02)
    while True:
        for i in range(-100, 51):
            GPG.set_motor_power(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, -i)
            time.sleep(0.02)
        
        for i in range(-50, 101):
            GPG.set_motor_power(GPG.MOTOR_LEFT + GPG.MOTOR_RIGHT, i)
            time.sleep(0.02)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    GPG.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the GoPiGo3 firmware.
