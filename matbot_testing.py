#matbot testing

import machine, time, math
from machine import Pin, PWM, ADC

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100 
from dcmotor import DCMotor
from servo import Servo

#enes100.begin("matbot", "MATERIAL", 328, 1201) # vision system setup #1120 normal room

sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 5000) # untrasonic distance sensor setup.

Pin1 = Pin(12, Pin.OUT)
Pin2 = Pin(13, Pin.OUT)
enable1 = PWM(Pin(14), 15000)

Pin3 = Pin(25, Pin.OUT)
Pin4 = Pin(26, Pin.OUT)
enable2 = PWM(Pin(27), 15000)

motor1 = DCMotor(Pin1, Pin2, enable1)
motor2 = DCMotor(Pin3, Pin4, enable2)

loadOUT = Pin(17, Pin.IN, pull=Pin.PULL_DOWN)
loadSCK = Pin(5, Pin.OUT)

claw_servo = Servo(pin_id=16)
lift_servo = Servo(pin_id=23)

claw_servo.write(70) #use 40 for grab, 70 for open
lift_servo.write(75) #prelift claw

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

hx711 = HX711(loadSCK, loadOUT)
hx711.tare()

# ----- tool functions -----

def where_am_i():
    if not enes100.is_visible:
        return [None, None, None]
   
    current_location = [enes100.x, enes100.y, enes100.theta]
    
    if current_location[2] < 0: #convert theta range of -pi -> pi to 0 -> 2pi
        current_location[2] = math.pi + (math.pi + current_location[2])
    return current_location

def object_detect(): # needs refining?
    distance = sensor.distance_cm()
    return distance #returns distance in CM

def angle_detect():
    pot_value = pot.read()
    return int(pot_value)

motor1.forward(12.5)

time.sleep(2)

motor1.forward(6)

time.sleep(2)

motor1.forward(1)