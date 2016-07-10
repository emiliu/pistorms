from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math

print "running program"

FOLLOW_SPEED = 8
SEARCH_SPEED = 70
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 6.5 # in

psm = PiStorms()
hc = HiTechnicColorV2()
psm.BBS2.activateCustomSensorI2C()
angle_pid = PIDController(-25, 25, 590.0, 0.16, 0.0, 0.0)
exit = False

'''
def turnDegs(degrees):
    theta = int(abs(2.0 * ROBOT_WIDTH * degrees / WHEEL_DIAMETER))
    print theta
    if degrees > 0:
        psm.BBM2.runDegs(theta, SEARCH_SPEED, True, False)
    else:
        psm.BBM1.runDegs(theta, SEARCH_SPEED, True, False)
    sleep(2)
'''

def turnDegs(degrees, left=True):
    theta = int(ROBOT_WIDTH * degrees / WHEEL_DIAMETER)
    print theta
    Thread(target = psm.BBM1.runDegs, args = (-1 * theta, SEARCH_SPEED, True, False)).start()
    Thread(target = psm.BBM2.runDegs, args = (theta, SEARCH_SPEED, True, False)).start()
    sleep(1.5)
    '''
    if left:
        psm.BBM1.runDegs(-1 * theta, SEARCH_SPEED, True, False)
    else:
        psm.BBM2.runDegs(theta, SEARCH_SPEED, True, False)
    '''

def goStraight(dist):
    theta = int(dist * 360 / WHEEL_DIAMETER / math.pi)
    psm.BBM1.runDegs(theta, SEARCH_SPEED, True, False)
    psm.BBM2.runDegs(theta, SEARCH_SPEED, True, False)
    print theta

def avoid():
    speed = 50
    psm.screen.termPrintln('obstacle')
    goStraight(-2)
    sleep(1)
    radius = 7
    turnDegs(-90)
    theta1 = int(radius * 360 / WHEEL_DIAMETER)
    theta2 = int((ROBOT_WIDTH + radius) * 360 / WHEEL_DIAMETER)
    psm.BBM1.runDegs(theta1, int(speed * radius / (ROBOT_WIDTH + radius)), True, False)
    psm.BBM2.runDegs(theta2, speed, True, False)
    sleep(1)
    turnDegs(-90)

def follow(e, f):
    while not exit and not e.isSet():
        if psm.BAS1.isTouchedNXT():
            psm.BBM1.brakeSync()
            avoid()
        value = psm.BBS1.lightSensorNXT(True)
        offset = angle_pid.calculate(value)
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(str(value) + ' ' + str(offset))
        psm.BBM1.setSpeed(FOLLOW_SPEED + offset)
        psm.BBM2.setSpeed(FOLLOW_SPEED - offset)
        sleep(0.1)
    while not exit and not f.isSet() and not psm.BAS1.isTouchedNXT():
        # enter house
        psm.BBM1.setSpeedSync(50)
        sleep(0.1)
    if not exit and not f.isSet():
        # face first room
        goStraight(-1)
        sleep(0.3)
        turnDegs(-90)
    if not exit and not f.isSet():
        # go into first room
        goStraight(6)
        sleep(0.5)
    if not exit and f.isSet():
        # check for bomb in first room
        goStraight(10)
        sleep(2)
        turnDegs(90)
        goStraight(18)
        sleep(2.5)
        return
    if not exit and not f.isSet():
        # back into second room
        goStraight(-31)
        sleep(3)
    if not exit and f.isSet():
        # check for bomb in second room
        turnDegs(90)
        goStraight(18)
        sleep(2.5)
        return
    if not exit and not f.isSet():
        # go in front of third room
        goStraight(11)
        sleep(2)
    if not exit and not f.isSet():
        # turn to face third room
        turnDegs(90)
    if not exit and not f.isSet():
        # enter third room
        goStraight(6)
        sleep(1)
    if not exit and f.isSet():
        # check for bomb in third room
        goStraight(8)
        sleep(1)
        turnDegs(-90)
        goStraight(12)
        sleep(2)
        return
    psm.BBM1.float()
    psm.BBM2.float()

def search(e, f):
    RED = 7         # or 8 or 9
    GREEN = 4
    PURPLE = 17     # also black o.O
    BLACK = 0
    while not exit:
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(psm.BBS1.lightSensorNXT(True)) #str(hc.get_colornum()))
        if not e.isSet():
            color = hc.get_colornum()
            if color > BLACK and color <= GREEN:
                psm.led(1, 0, 255, 0)
                psm.screen.termPrintln('found victim')
                sleep(3)
                psm.led(1, 0, 0, 0)
                sleep(2)
            elif color >= RED and color <= RED + 2:
                e.set()
                psm.screen.termPrintln('e.set()')
                print 'e.set()'
        elif not f.isSet():
            color = hc.get_colornum()
            light = psm.BBS1.lightSensorNXT(True)
            if color > BLACK and color <= GREEN:
                f.set()
                psm.led(1, 255, 0, 0)
                psm.screen.termPrintln('f.set()')
                print 'f.set()'
        sleep(0.1)
    psm.led(1, 0, 0, 0)


if __name__ == "__main__":

    entered_house = Event()
    found_bomb = Event()

    f_thread = Thread(target=follow, args=(entered_house, found_bomb))
    f_thread.start()
    s_thread = Thread(target=search, args=(entered_house, found_bomb))
    s_thread.start()

    while not exit:

        sleep(0.05)

        if psm.isKeyPressed(): # if the GO button is pressed
            psm.screen.clearScreen()
            psm.screen.termPrintln("Exiting to menu")
            psm.led(1,0,0,0)    
            psm.BAM1.float()
            psm.BAM2.float()
            psm.BBM1.float()
            psm.BBM2.float() 
            sleep(0.1)
            exit = True
