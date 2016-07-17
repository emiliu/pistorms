from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math

print 'running program'
exit = False

psm = PiStorms()
if not psm.BAS1.presenceUSEV3():
    print 'no ultrasonic sensor'
    exit = True

def go():
    while not exit:
        psm.screen.termPrintln('%d     %f' % (psm.BAS1.lightSensorNXT(True), psm.BBS1.distanceUSEV3in()))
        '''
        if psm.BAS1.lightSensorNXT(True) > 550:
            psm.BBM1.setSpeed(100)
            psm.BBM2.setSpeed(-100)
        elif psm.BBS1.distanceUSEV3in() < 30:
            psm.BBM1.setSpeedSync(100)
        else:
            psm.BBM1.setSpeed(80)
            psm.BBM2.setSpeed(50)
        '''
        sleep(0.1)
    psm.BAM1.float()
    psm.BAM2.float()

def ramp():
    pass


if __name__ == '__main__':

    Thread(target = go).start()

    while not exit:
        sleep(0.05)

    if psm.isKeyPressed():
          psm.screen.clearScreen()
          psm.screen.termPrintln("")
          psm.screen.termPrintln("Exiting to menu")
          psm.led(1,0,0,0)    
          sleep(0.1)
          exit = True
