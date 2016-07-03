from PiStorms import PiStorms
from time import sleep
print "running program"
psm = PiStorms()

psm.BBM1.setSpeed(-75)
psm.BBM2.setSpeed(-75)
sleep(1.5)
psm.BBM1.setSpeed(75)
psm.BBM2.setSpeed(-75)
sleep(1)
psm.BBM1.brake()
psm.BBM2.brake()
