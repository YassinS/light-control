from core.sh_io import Led, Button, Switch
from core.sh_system import Program
from time import sleep, time

import pigpio

a1 = Led("LED1", "LED", "1", {}, 20)
b1 = Button("BTN1", "BUTTON", "2", {}, 19)
s1 = Switch([b1], [a1])

a1.setup()
b1.setup()

while True:
    s1.execute()
