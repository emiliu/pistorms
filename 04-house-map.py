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

   # go straight for 8 inches
   # left : bbm1
   # left motor turns 90 degree
   # go straight for 12 inches

  if(color sensor sees red)
    psm.BBM2.setSpeed(50)
    sleep(60)
    psm.BBM2.runDegs(90,20,False,True)
    psm.BBM2.setSpeed(50)
    psm.BBM1.setSpeed(50)
    sleep(120)
   #go toward green line for 4 inches
   # turn around 180 degrees
   # go straight
  if(color sensor sees green)
    psm.BBM2.setSpeed(50)
    psm.BBM1.setSpeed(50)
    sleep(60)
    psm.BBM1.runDegs(180,20,False,False)
    psm.BBM2.setSpeed(50)
    psm.BBM1.setSpeed(50)
    sleep(500)
  # go toward blue line for 4 inches
   # turn around 180 degrees
    #go straight
   # every inch turn 20 degrees to left turn 20 degrees to left
  if(color sensor sees blue)
     psm.BBM2.setSpeed(50)
    psm.BBM1.setSpeed(50)
    sleep(60)
    psm.BBM1.runDegs(180,20,False,False)
    psm.BBM2.setSpeed(50)
    psm.BBM1.setSpeed(50)
    sleep(60)
  if(color sensor sees red)
    go toward red line for 4 inches

  
