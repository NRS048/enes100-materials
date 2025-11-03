import machine, time
from machine import Pin

from enes100 import enes100

enes100.begin(team_name: "matbot", team_type: "MATERIAL", aruco_id: 328, room_num: 1120)

Pin5 = Pin(23, Pin.OUT) # 5v power for motor driver
Pin5.value(1)

Pin1 = Pin(12, Pin.OUT)
Pin2 = Pin(13, Pin.OUT)
enable1 = PWM(Pin(14), 15000)

Pin3 = Pin(25, Pin.OUT)
Pin4 = Pin(26, Pin.OUT)
enable2 = PWM(Pin(27), 15000)

motor1 = DCMotor(Pin1, Pin2, enable1)
motor2 = DCMotor(Pin3, Pin4, enable2)

motor1.backward(25)
motor2.formard(25)

time.sleep(2)

motor1.stop()
motor2.stop()