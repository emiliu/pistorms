from PiStorms import PiStorms
from time import sleep
print "running program"
psm = PiStorms()

exit = False

while not exit:

    psm.BBM1.setSpeed(35)
    psm.BBM2.setSpeed(60)
    sleep(0.1)

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
