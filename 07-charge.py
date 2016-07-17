from PiStorms import PiStorms
from HiTechnicColorV2 import HiTechnicColorV2
from time import sleep
from threading import Thread, Event
from pid import PIDController
import math

print 'running program'
exit = False

psm = PiStorms()
'''
if not psm.BAS2.presenceUSEV3():
    psm.screen.termPrintln('no ultrasonic sensor')
    print 'no ultrasonic sensor'
    exit = True
'''

EDGE_LIGHT = 650
RAMP_DIST = 45
RUSH_DIST = 300
RAMP_ANGLE = 115    # actually 120, but with some leeway
                    # also, negative is up


def ramp(angle):
    psm.BAM1.runDegs(angle, 80, True, True)
    while psm.BAM1.isBusy():
        pass
    return


def go():
    while not exit:
        psm.screen.termPrintln(str(psm.BAS1.lightSensorNXT(True)) + '   ' + str(psm.BAS2.distanceUSEV3in()) + '    ' + str(psm.BAM1.pos()))
        if psm.BAS1.lightSensorNXT(True) > EDGE_LIGHT:
            psm.BBM1.setSpeed(100)
            psm.BBM2.setSpeed(-100)
            ramp(-1 * RAMP_ANGLE)
        elif psm.BAS2.distanceUSEV3in() < RUSH_DIST:
            psm.BBM1.setSpeedSync(100)
            ramp(RAMP_ANGLE)
        else:
            psm.BBM1.setSpeed(80)
            psm.BBM2.setSpeed(50)
        sleep(0.1)
    psm.BBM1.float()
    psm.BBM2.float()


if __name__ == '__main__':

    psm.BAM1.resetPos()

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
