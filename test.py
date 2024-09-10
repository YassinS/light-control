from core.sh_io import Led, Button, Switch, MotionDetector
from core.sh_system import Program
from time import sleep, time

import pigpio

a1 = Led("LED1", "LED", "1", {}, 20)
b1 = Button("BTN1", "BUTTON", "2", {}, 19)
m1 = MotionDetector("MTND1", "MOTIONDETECTOR", "3", {}, 12)
s1 = Switch([b1], [a1])

a1.setup()
b1.setup()
m1.setup()
