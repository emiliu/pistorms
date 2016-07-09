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

#exit variable will be used later to exit the program and return to PiStorms
exit = False

def follow(e, f):
    speed = 8
    while not exit and not e.isSet():
        value = psm.BBS1.lightSensorNXT(True)
        offset = angle_pid.calculate(value)
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(str(value) + ' ' + str(offset))
        psm.BBM1.setSpeed(speed + offset)
        psm.BBM2.setSpeed(speed - offset)
        sleep(0.1)
    while not exit and not f.isSet():
        psm.BBM1.setSpeedSync(20)
        sleep(0.1)
    psm.BBM1.float()
    psm.BBM2.float()

def search(e, f):
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
        elif not f.isSet():
            if color > BLACK and color <= GREEN:
                f.set()
                psm.led(1, 255, 0, 0)
                psm.screen.termPrintln('f.set()')
                print 'f.set()'
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
