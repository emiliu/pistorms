from PiStorms import PiStorms
'''
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math
'''
from threading import Thread
from time import sleep

print "running program"

SEARCH_SPEED = 50
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 6.5 # in

psm = PiStorms()

def turnDegs(degrees, left=True):
    theta = int(ROBOT_WIDTH * degrees / WHEEL_DIAMETER)
    print theta
    if left:
        psm.BBM1.runDegs(-1 * theta, SEARCH_SPEED, True, False)
    else:
        psm.BBM2.runDegs(theta, SEARCH_SPEED, True, False)

def leftMotor():
    turnDegs(180, True)
    sleep(1)

def rightMotor():
    turnDegs(180, False)
    sleep(1)

left = Thread(target = leftMotor)
left.start()
right = Thread(target = rightMotor)
right.start()
