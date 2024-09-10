import random
from datetime import datetime, time
import pigpio
import time as t


class Device:
    def __init__(self, name, device_type, device_id, device_info, pin):
        self.name = name
        self.device_type = device_type
        self.device_id = device_id
        self.device_info = device_info
        self.device_state = False
        self.pin = pin
        self.is_set_up = False
        self.pi = pigpio.pi()

    def __str__(self) -> str:
        return f"{self.name} ({self.device_type})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.device_type})"

    def get_is_set_up(self) -> bool:
        return self.is_set_up

    def get_device_type(self) -> str:
        return self.device_type

    def get_device_id(self) -> str:
        return self.device_id

    def get_device_info(self) -> dict:
        return self.device_info

    def get_device_state(self) -> bool:
        return self.device_state

    def get_pin(self) -> int:
        return self.pin

    def get_name(self) -> str:
        return self.name

    def set_pin(self, pin: int) -> None:
        self.pin = pin

    def set_name(self, name: str) -> None:
        self.name = name

    def set_device_type(self, device_type: str) -> None:
        self.device_type = device_type

    def set_device_id(self, device_id: str) -> None:
        self.device_id = device_id

    def set_device_info(self, device_info: dict) -> None:
        self.device_info = device_info

    def set_device_state(self, device_state: bool) -> None:
        self.device_state = device_state

    def set_is_set_up(self, val: bool):
        self.is_set_up = val


class Sensor(Device):
    def __init__(self, name, device_type, device_id, device_info, pin):
        super().__init__(name, device_type, device_id, device_info, pin)
        self.value = 0

    def __str__(self) -> str:
        return f"Sensor: {super().__str__()}"

    def __repr__(self) -> str:
        return f"Sensor: {super().__repr__()}"

    def is_higher(self):
        return Condition(self, ">")

    def is_lower(self, sensor):
        return Condition(self, "<")

    def is_equal(self, sensor):
        return Condition(self, "==")

    def read(self):
        if self.is_set_up:
            return self.pi.read(self.pin)
        else:
            raise Exception("Sensor is not set up")

    def setup(self):
        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.is_set_up = True

    def update(self):
        if self.is_set_up:
            self.value = self.pi.read(self.pin)
        else:
            raise Exception("Sensor is not set up")


class Actor(Device):
    def __init__(self, name, device_type, device_id, device_info, pin):
        super().__init__(name, device_type, device_id, device_info, pin)

    def __str__(self) -> str:
        return f"Actor: {super().__str__()}"

    def __repr__(self) -> str:
        return f"Actor: {super().__repr__()}"

    def setup(self):
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.is_set_up = True

    def on(self):
        if self.is_set_up:
            self.pi.write(self.pin, 1)
        else:
            raise Exception("Actor is not set up")

    def off(self):
        if self.is_set_up:
            self.pi.write(self.pin, 0)
        else:
            raise Exception("Actor is not set up")


class MotionDetector(Sensor):
    def __init__(self, name, device_type, device_id, device_info, pin):
        super().__init__(name, device_type, device_id, device_info, pin)

    def setup(self):
        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.is_set_up = True

    def is_motion_detected(self):
        if self.is_set_up:
            return self.pi.read(self.pin) == 1
        else:
            raise Exception("Motion detector is not set up")


class Button(Sensor):
    def __init__(self, name, device_type, device_id, device_info, pin):
        super().__init__(name, device_type, device_id, device_info, pin)

    def __str__(self) -> str:
        return f"Button: {super().__str__()}"

    def __repr__(self) -> str:
        return f"Button: {super().__repr__()}"

    def setup(self):
        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.is_set_up = True

    def is_pressed(self) -> bool:
        if self.is_set_up:
            return self.pi.read(self.pin) == 1
        else:
            raise Exception("Button is not set up")


class Led(Actor):
    def __init__(self, name, device_type, device_id, device_info, pin):
        super().__init__(name, device_type, device_id, device_info, pin)

    def __str__(self) -> str:
        return f"LED: {super().__str__()}"

    def __repr__(self) -> str:
        return f"LED: {super().__repr__()}"

    def blink(self, interval: int = 2, iterations: int = 3):
        if self.is_set_up:
            for i in range(0, iterations):
                self.on()
                t.sleep(interval)
                self.off()
                t.sleep(interval)
        else:
            raise Exception("LED is not set up")

    def setup(self):
        self.pi.set_mode(self.pin, pigpio.OUTPUT)
        self.is_set_up = True


class Constant:
    def __init__(self, value: int):
        self.value = value

    def is_equal_to(self, sensor: Sensor) -> bool:
        return sensor.read() == self.value

    def is_greater_than(self, sensor: Sensor) -> bool:
        return sensor.read() > self.value

    def is_less_than(self, sensor: Sensor) -> bool:
        return sensor.read() < self.value

    def is_in_range(self, sensor: Sensor, lower: int, upper: int) -> bool:
        return lower <= sensor.read() <= upper


class Condition:
    def __init__(self, sensor: Sensor, operator: str, compare_to=None):
        self.sensor = sensor
        self.operator = operator
        self.compare_to = compare_to

    def than(self, other):
        self.compare_to = other
        return self

    def evaluate(self) -> bool:
        if isinstance(self.compare_to, Sensor):
            if self.operator == ">":
                return self.sensor.read() > self.compare_to.read()
            elif self.operator == "<":
                return self.sensor.read() < self.compare_to.read()
            elif self.operator == "==":
                return self.sensor.read() == self.compare_to.read()
        elif isinstance(self.compare_to, Constant):
            if self.operator == ">":
                return self.compare_to.is_greater_than(self.sensor)
            elif self.operator == "<":
                return self.compare_to.is_less_than(self.sensor)
            elif self.operator == "==":
                return self.compare_to.is_equal_to(self.sensor)
            elif self.operator == "in_range":
                return self.compare_to.is_in_range(self.sensor, *self.compare_to.value)
        return False


class TimeCondition:
    def __init__(self, target_time=None, start_time=None, end_time=None):
        self.target_time = target_time
        self.start_time = start_time
        self.end_time = end_time

    def is_time(self) -> bool:
        current_time = datetime.now().time()
        if self.target_time:
            return current_time >= self.target_time
        elif self.start_time and self.end_time:
            return self.start_time <= current_time <= self.end_time
        return False


"""
This serves as a base class for all circuits.
"""


class Circuit:
    def __init__(self, sensors: list, actors: list) -> None:
        self.sensors = sensors
        self.actors = actors

    def execute(self):
        pass


class Switch(Circuit):
    def __init__(self, sensors: list, actors: list):
        super().__init__(sensors, actors)
        self.a = actors[0]
        self.s = sensors[0]
        self.old_btn = False
        self.state = False

    def execute(self):
        if self.s.is_pressed() and not self.old_btn:
            if not self.state:
                self.state = True
                self.a.on()
            else:
                self.a.off()
                self.state = False
            self.old_btn = True
        elif not self.s.is_pressed() and self.old_btn:
            self.old_btn = False
