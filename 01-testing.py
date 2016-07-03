from PiStorms import PiStorms
from time import sleep
print "running program"
psm = PiStorms()

psm.BBM1.setSpeed(50);
psm.BBM2.setSpeed(50);
sleep(1);
psm.BBM1.setSpeed(0);
psm.BBM2.setSpeed(0);
