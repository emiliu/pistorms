from PiStorms import PiStorms
'''
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math
'''

print "running program"

SEARCH_SPEED = 50
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 6.5 # in

psm = PiStorms()

def turnDegs(degrees):
    theta = int(abs(2.0 * ROBOT_WIDTH * degrees / WHEEL_DIAMETER))
    print theta
    if degrees > 0:
        psm.BBM2.runDegs(theta, SEARCH_SPEED, True, False)
    else:
        psm.BBM1.runDegs(theta, SEARCH_SPEED, True, False)

turnDegs(180)
