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
RUSH_DIST = 80
RAMP_UP = -115      # actually 120, but with some leeway
RAMP_MID = -50      # approximately
RAMP_DOWN = 0       # also, negative is up
SEARCH_SPEED = 50
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 5.0 # in

def turnDegs(degrees, left=True):
    theta = int(ROBOT_WIDTH * degrees / WHEEL_DIAMETER)
    print theta
    Thread(target = psm.BAM1.runDegs, args = (-1 * theta, SEARCH_SPEED, True, False)).start()
    Thread(target = psm.BAM2.runDegs, args = (theta, SEARCH_SPEED, True, False)).start()
    while psm.BAM1.isBusy():
        pass

def ramp(angle):
    #psm.BAM1.runDegs(angle, 80, True, True)
    #while psm.BAM1.isBusy():
        #pass
    return


def go():
    while not exit:
        psm.screen.termPrintln(str(psm.BAS1.lightSensorNXT(True)) + '   ' + str(psm.BAS2.distanceUSEV3in()) + '    ' + str(psm.BAM1.pos()))

        # reached edge
        if psm.BAS1.lightSensorNXT(True) < EDGE_LIGHT:
            psm.BBM1.setSpeedSync(-50)
            sleep(0.5)
            turnDegs(180)
            #ramp(RAMP_MID)

        # saw someone
        elif psm.BAS2.distanceUSEV3in() < RUSH_DIST:
            psm.BBM1.setSpeedSync(50)
            #ramp(RAMP_DOWN)

        # driving around
        else:
            psm.BBM1.setSpeed(20)
            psm.BBM2.setSpeed(50)
            #ramp(RAMP_MID)

        sleep(0.1)

    psm.BBM1.float()
    psm.BBM2.float()


if __name__ == '__main__':

    psm.BAM1.resetPos()
    psm.BAM1.hold()

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
