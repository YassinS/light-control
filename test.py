from core.sh_io import Led, Button
from core.sh_system import Program
from time import sleep, time

import pigpio

a1 = Led("LED1", "LED", "1", {}, 20)
b1 = Button("BTN1", "BUTTON", "2", {}, 19)

a1.setup()
b1.setup()

a1.on()

old_btn = False
state = False

while True:
    if b1.is_pressed() and not old_btn:
        if not state:
            state = True
            a1.on()
        else:
            a1.off()
            state = False
        old_btn = True
    elif not b1.is_pressed() and old_btn:
        old_btn = False
