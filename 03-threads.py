from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math

print "running program"

psm = PiStorms()
hc = HiTechnicColorV2()
psm.BBS2.activateCustomSensorI2C()
angle_pid = PIDController(-25, 25, 590.0, 0.05, 0.0, 0.0)
exit = False


def toDegs(dist, dia):
    return int(float(dist) / dia * 360)

def follow(e, f, g):
    FOLLOW_SPEED = 8
    SEARCH_SPEED = 80
    WHEEL_DIA = 3.0 # in
    ROBOT_WID = 6.0 # in
    while not exit and not e.isSet():
        value = psm.BBS1.lightSensorNXT(True)
        offset = angle_pid.calculate(value)
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(str(value) + ' ' + str(offset))
        psm.BBM1.setSpeed(FOLLOW_SPEED + offset)
        psm.BBM2.setSpeed(FOLLOW_SPEED - offset)
        sleep(0.1)
    if not exit and not f.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.5)
        psm.BBM1.brakeSync()
        psm.BBM1.runDegs(toDegs(ROBOT_WID * math.PI * 0.5, WHEEL_DIA), SEARCH_SPEED, True, True)
    while not exit and not f.isSet() and not g.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.1)
    sleep(0.1)
    if not exit and not f.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.5)
        psm.BBM1.brakeSync()
        psm.BBM1.runDegs(toDegs(ROBOT_WID * math.PI, WHEEL_DIA), SEARCH_SPEED, True, True)
    while not exit and not f.isSet() and not g.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.1)
    sleep(0.1)
    if not exit and not f.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.5)
        psm.BBM1.brakeSync()
        psm.BBM1.runDegs(toDegs(ROBOT_WID * math.PI, WHEEL_DIA), SEARCH_SPEED, True, True)
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.5)
        psm.BBM2.runDegs(toDegs(ROBOT_WID * math.PI * 0.5, WHEEL_DIA), SEARCH_SPEED, True, True)
    while not exit and not f.isSet() and not g.isSet():
        psm.BBM1.setSpeedSync(SEARCH_SPEED)
        sleep(0.1)
    sleep(0.1)
    psm.BBM1.float()
    psm.BBM2.float()

def search(e, f, g):
    RED = 7         # or 8 or 9
    GREEN = 4
    PURPLE = 17     # also black o.O
    BLACK = 0
    while not exit:
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(str(hc.get_colornum()))
        color = hc.get_colornum()
        if not e.isSet():
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
            if color > BLACK and color <= GREEN:
                f.set()
                g.set()
                psm.led(1, 255, 0, 0)
                psm.screen.termPrintln('f.set()')
                print 'f.set()'
            elif color >= PURPLE:
                g.set()
                sleep(0.1)
                g.clear()
        sleep(0.1)
    psm.led(1, 0, 0, 0)

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
