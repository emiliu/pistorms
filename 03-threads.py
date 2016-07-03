from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
import math

print "running program"
psm = PiStorms()
hc = HiTechnicColorV2()
psm.BBS2.activateCustomSensorI2C()

#exit variable will be used later to exit the program and return to PiStorms
exit = False

def follow(e):
    speed = 20
    threshold = 600
    threshold_ = 20
    scale = 5
    while not exit and not e.isSet():
        value = psm.BBS1.lightSensorNXT(True)
        offset = math.copysign(1, value - threshold) * scale if abs(value - threshold) > threshold_ else 0
        psm.screen.clearScreen()
        psm.screen.termPrintln(str(value) + ' ' + str(offset))
        psm.BBM1.setSpeed(speed - offset)
        psm.BBM2.setSpeed(speed + offset)
    psm.BAM1.float()
    psm.BAM2.float()
    psm.BBM1.float()
    psm.BBM2.float() 

def search(e, f):
    RED = 7         # or 8 or 9
    GREEN = 4
    PURPLE = 17     # also black o.O
    while not exit:
        #psm.screen.clearScreen()
        #psm.screen.termPrintln(str(hc.get_colornum()))
        color = hc.get_colornum()
        if color <= GREEN:
            if not e.isSet():
                psm.led(1, 255, 0, 0)
                sleep(3)
                psm.led(1, 0, 0, 0)
                sleep(2)
            elif not f.isSet():
                f.set()
        elif color >= RED and color <= RED + 2:
            e.set()
        sleep(0.1)
        psm.led(1, 0, 0, 0)

entered_house = Event()
found_bomb = Event()

f_thread = Thread(target=follow, args=(entered_house,))
f_thread.start()
s_thread = Thread(target=search, args=(entered_house, found_bomb))
s_thread.start()

while(not exit):

    #line_follow()
    #find_victims()

    if(psm.isKeyPressed() == True): # if the GO button is pressed
        psm.screen.clearScreen()
        psm.screen.termPrintln("Exiting to menu")
        psm.led(1,0,0,0)    
        psm.BAM1.float()
        psm.BAM2.float()
        psm.BBM1.float()
        psm.BBM2.float() 
        sleep(0.1)
        exit = True

    sleep(0.05)