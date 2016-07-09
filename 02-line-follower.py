from PiStorms import PiStorms
from time import sleep
from HiTechnicColorV2 import HiTechnicColorV2
from threading import Thread
from pid import PIDController
#from math import copysign

print "running program"
psm = PiStorms()
'''
hc = HiTechnicColorV2()
psm.BBS1.activateCustomSensorI2C()
'''

angle_pid = PIDController(-25, 25, 590.0, 0.05, 0.0, 0.0)

#exit variable will be used later to exit the program and return to PiStorms
exit = False

def line_follow():
    speed = 8
    #threshold = 600
    #threshold_ = 20
    #scale = 3
    while not exit:
        value = psm.BBS1.lightSensorNXT(True)
        #offset = math.copysign(1, value - threshold) * scale if abs(value - threshold) > threshold_ else 0
        offset = angle_pid.calculate(value)
        psm.screen.clearScreen()
        psm.screen.termPrintln(str(value) + ' ' + str(offset))
        psm.BBM1.setSpeed(speed + offset)
        psm.BBM2.setSpeed(speed - offset)
        sleep(0.05)
    psm.BBM1.float()
    psm.BBM2.float()

'''
def find_victims():
    while not exit:
        color = hc.get_colornum()
        if color == 9 or color == 8:
            psm.led(1, 255, 0, 0)
            sleep(3)
            psm.led(1, 0, 0, 0)
            sleep(2)
        sleep(0.1)
        psm.led(1, 0, 0, 0)
'''

lf = Thread(target=line_follow)
lf.start()
#fv = Thread(target=find_victims)
#fv.start()

while not exit:

    if(psm.isKeyPressed() == True): # if the GO button is pressed
        exit = True
        sleep(0.1)
        psm.screen.clearScreen()
        psm.screen.termPrintln("Exiting to menu")
        psm.led(1,0,0,0)    
        psm.BAM1.float()
        psm.BAM2.float()
        psm.BBM1.float()
        psm.BBM2.float() 

    sleep(0.05)
