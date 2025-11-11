import machine, time
from machine import Pin, PWM
from time import sleep
from enes100 import enes100

from servo import Servo

#enes100.begin("matbot", "MATERIAL", 328, 1120)#1120 normal, 1116 aux

my_servo = Servo(pin_id=5)
my_servo.write(0)

time.sleep(2)

my_servo.write(90)

time.sleep(2)

my_servo.write(0)

#i = 1
#while i <= 30:
#    i += 1
#    my_servo.write(90-i)
#    time.sleep(.125)