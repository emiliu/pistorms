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
RUSH_DIST = 40
RAMP_UP = -115      # actually 120, but with some leeway
RAMP_MID = -60      # approximately
RAMP_DOWN = 0       # also, negative is up
SPEED = 45
WHEEL_DIAMETER = 2.25 # in
ROBOT_WIDTH = 4.0 # in

def turnDegs(degrees, left=True):
    theta = int(ROBOT_WIDTH * degrees / WHEEL_DIAMETER)
    print theta
    Thread(target = psm.BBM1.runDegs, args = (-1 * theta, SPEED, True, False)).start()
    Thread(target = psm.BBM2.runDegs, args = (theta, SPEED, True, False)).start()

def ramp(angle):
    psm.BAM1.runDegs(angle - psm.BAM1.pos(), 80, True, True)


def go():
    while not exit:
        #psm.screen.termPrintln(str(psm.BAS1.lightSensorNXT(True)) + '   ' + str(psm.BAS2.distanceUSEV3in()) + '    ' + str(psm.BAM1.pos()))

        # reached edge
        if psm.BAS1.lightSensorNXT(True) < EDGE_LIGHT:
            psm.BBM1.brakeSync()
            ramp(RAMP_MID)
            psm.BBM1.setSpeedSync(-1 * SPEED)
            sleep(1)
            psm.BBM1.brakeSync()
            turnDegs(100)
            sleep(1)

        # saw someone
        elif psm.BAS2.distanceUSEV3in() < RUSH_DIST:
            ramp(RAMP_DOWN)
            psm.BBM1.setSpeedSync(SPEED)

        # driving around
        else:
            ramp(RAMP_MID)
            psm.BBM1.setSpeedSync(SPEED)

        sleep(0.1)

    psm.BAM1.float()
    psm.BAM2.float()
    psm.BBM1.float()
    psm.BBM2.float()


if __name__ == '__main__':

    psm.BAM1.resetPos()
    ramp(RAMP_UP)

    while not psm.isKeyPressed():
        psm.screen.termPrintln('waiting')

    psm.screen.clearScreen()
    psm.screen.termPrintln('starting!')

    for i in xrange(5):
        psm.led(1, 255, 0, 0)
        sleep(0.8)
        psm.led(1, 0, 0, 0)
        sleep(0.2)

    psm.screen.clearScreen()
    ramp(RAMP_MID)
    sleep(0.5)

    Thread(target = go).start()

    while not exit:
        sleep(0.05)

        if psm.isKeyPressed():
              psm.screen.clearScreen()
              psm.screen.termPrintln("")
              psm.screen.termPrintln("Exiting to menu")
              psm.led(1,0,0,0)    
              psm.BAM1.float()
              psm.BAM2.float()
              psm.BBM1.float()
              psm.BBM2.float()
              sleep(0.1)
              exit = True
