from core.sh_io import Sensor, Actor, Condition
from time import time


class Program:
    def __init__(self):
        self.sensors = []
        self.actors = []
        self.condition = None
        self.action = None
        self.time_condition = None

    def set_sensors(self, sensors: list):
        self.sensors = sensors

    def set_actors(self, actors: list):
        self.actors = actors

    def get_sensors(self) -> list:
        return self.sensors

    def get_actors(self) -> list:
        return self.actors

    def get_time_condition(self):
        return self.time_condition

    def set_time_condition(self, time_condition):
        self.time_condition = time_condition

    def set_condition(self, condition: Condition):
        self.condition = condition

    def set_action(self, action):
        self.action = action

    def setup(self):
        for sensor in self.sensors:
            sensor.setup()
            print(sensor.read())  # debug

        for actor in self.actors:
            actor.setup()

    def execute(self):
        if self.condition and self.action:
            if self.condition.evaluate():
                self.action()
        if self.time_condition and self.action:
            if self.time_condition.is_time():
                self.action()
