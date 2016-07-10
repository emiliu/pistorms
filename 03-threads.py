from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math

print "running program"

FOLLOW_SPEED = 15
SEARCH_SPEED = 20
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 6.5 # in

psm = PiStorms()
hc = HiTechnicColorV2()
psm.BBS2.activateCustomSensorI2C()
angle_pid = PIDController(-25, 25, 590.0, 0.1, 0.0, 0.0)
exit = False

bomb = 0

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
    sleep(3)
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
    psm.screen.termPrintln('hi')
    #theta = int(
    #Thread(target = psm.BBM1

def follow(e, f, g):
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
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.1)
    psm.BBM1.brakeSync()
    if not exit and not f.isSet():
        # face first room
        psm.BBM1.setSpeedSync(-1 * SEARCH_SPEED)
        sleep(0.3)
        psm.BBM1.brakeSync()
        turnDegs(-90)
    if not exit and not f.isSet():
        # go into first room
        goStraight(6)
        sleep(2)
    if not exit and not f.isSet() and not g.isSet():
        # back into second room
        goStraight(-30)
        sleep(10)
    psm.BBM1.brakeSync()
    if not exit and not f.isSet():
        # go in front of third room
        goStraight(6)
        sleep(2)
    if not exit and not f.isSet():
        # turn to face third room
        turnDegs(90)
    if not exit and not f.isSet() and not g.isSet():
        # enter third room
        goStraight(6)
        sleep(2)
    while not exit: # and bomb (not bomb room) not found
        psm.BBM1.float()
        psm.BBM2.float()
        if bomb == 1:
            pass
        # etc
        sleep(0.1)
    psm.BBM1.float()
    psm.BBM2.float()

def search(e, f, g):
    global bomb
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
        elif not f.isSet() and not g.isSet():
            color = hc.get_colornum()
            light = psm.BBS1.lightSensorNXT(True)
            if color > BLACK and color <= GREEN:
                f.set()
                g.set()
                psm.led(1, 255, 0, 0)
                psm.screen.termPrintln('f.set()')
                bomb += 1
                print 'f.set(), bomb = ' + str(bomb)
                sleep(3)
            elif light < 750: #color >= PURPLE:
                g.set()
                bomb += 1
                print 'g.set(), bomb = ' + str(bomb)
                sleep(0.2)
                g.clear()
                sleep(4)
        sleep(0.1)
    psm.led(1, 0, 0, 0)


if __name__ == "__main__":

    entered_house = Event()
    found_bomb = Event()
    gone_room = Event()

    f_thread = Thread(target=follow, args=(entered_house, found_bomb, gone_room))
    f_thread.start()
    s_thread = Thread(target=search, args=(entered_house, found_bomb, gone_room))
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
