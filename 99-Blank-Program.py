from PiStorms import PiStorms
from time import sleep
print "running program"
psm = PiStorms()

#exit variable will be used later to exit the program and return to PiStorms
exit = False

while(not exit):

#put your cool code here
# I will turn a light on

  psm.led(1,255,0,255) 
  sleep(0.25)

  if(psm.isKeyPressed() == True): # if the GO button is pressed
    psm.screen.clearScreen()
    psm.screen.termPrintln("")
    psm.screen.termPrintln("Exiting to menu")
    psm.led(1,0,0,0)    
    sleep(0.5)
    exit = True



