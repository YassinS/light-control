import random
from datetime import datetime, time


class Device:
    def __init__(self, name, device_type, device_id, device_info):
        self.name = name
        self.device_type = device_type
        self.device_id = device_id
        self.device_info = device_info
        self.device_state = dict()

    def __str__(self) -> str:
        return f"{self.name} ({self.device_type})"

    def __repr__(self) -> str:
        return f"{self.name} ({self.device_type})"

    def get_name(self) -> str:
        return self.name

    def get_device_type(self) -> str:
        return self.device_type

    def get_device_id(self) -> str:
        return self.device_id

    def get_device_info(self) -> dict:
        return self.device_info

    def get_device_state(self) -> dict:
        return self.device_state

    def set_name(self, name: str) -> None:
        self.name = name

    def set_device_type(self, device_type: str) -> None:
        self.device_type = device_type

    def set_device_id(self, device_id: str) -> None:
        self.device_id = device_id

    def set_device_info(self, device_info: dict) -> None:
        self.device_info = device_info

    def set_device_state(self, device_state: dict) -> None:
        self.device_state = device_state


class Sensor(Device):
    def __init__(self, name, device_type, device_id, device_info):
        super().__init__(name, device_type, device_id, device_info)
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
        return self.value

    def setup(self):
        self.value = random.randint(0, 100)
        pass

    def update(self):
        self.value = random.randint(0, 100)

    def listen(self):
        pass


class Actor(Device):
    def __init__(self, name, device_type, device_id, device_info):
        super().__init__(name, device_type, device_id, device_info)

    def __str__(self) -> str:
        return f"Actor: {super().__str__()}"

    def __repr__(self) -> str:
        return f"Actor: {super().__repr__()}"

    def setup(self):
        pass


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
