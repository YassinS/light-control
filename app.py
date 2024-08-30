from core.sh_system import Program
from core.sh_io import Sensor, Actor, Constant, TimeCondition
import time
import datetime

program = Program()
program2 = Program()

# Define sensors
s1 = Sensor("Temperature Sensor", "temperature", "1", {"unit": "C"})
s2 = Sensor("Humidity Sensor", "humidity", "2", {"unit": "%"})
s3 = Sensor("Light Sensor", "light", "3", {"unit": "lux"})
for sensor in [s1, s2, s3]:
    sensor.setup()
    print(sensor.read())


# Define actors
a1 = Actor("Heater", "heater", "1", {"unit": "C"})
a2 = Actor("Cooler", "cooler", "2", {"unit": "C"})
a3 = Actor("Light", "light", "3", {"unit": "lux"})


# Set sensors and actors
program.set_sensors([s1, s2, s3])
program.set_actors([a1, a2, a3])

# Define conditions
program.set_condition(
    program.get_sensors()[0].is_higher().than(program.get_sensors()[1])
)

# Define actions

a = lambda: print("Action executed")

program.set_action(a)

program.execute()


c1 = Constant(30)

program2.set_sensors([s1, s2, s3])
program2.set_actors([a1, a2, a3])

program2.setup()

program2.set_condition(program2.get_sensors()[0].is_higher().than(c1))
a2 = lambda: print(
    f"Temperature {program2.get_sensors()[0].read()} is higher than {c1.value}"
)
program2.set_action(a2)

program2.execute()


program3 = Program()

start = datetime.time(14, 30)
end = datetime.time(15, 0)

t1 = TimeCondition(start_time=start, end_time=end)
program3.set_sensors([s1])
program3.set_actors([a1])

program3.set_time_condition(t1)
program3.set_action(lambda: print("Time triggered action"))

program3.setup()


# Main loop

while True:
    for sensor in program.get_sensors():
        sensor.update()

    for sensor in program2.get_sensors():
        sensor.update()

    program.execute()
    program2.execute()
    program3.execute()
    time.sleep(1)
