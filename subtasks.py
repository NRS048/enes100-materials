import machine, time
from machine import Pin

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100

enes100.begin("matbot", "MATERIAL", 328, 1120)

sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 10000)

Pin1 = Pin(12, Pin.OUT)
Pin2 = Pin(13, Pin.OUT)
enable1 = PWM(Pin(14), 15000)

Pin3 = Pin(25, Pin.OUT)
Pin4 = Pin(26, Pin.OUT)
enable2 = PWM(Pin(27), 15000)

motor1 = DCMotor(Pin1, Pin2, enable1)
motor2 = DCMotor(Pin3, Pin4, enable2)

loadOUT = pin( , Pin.IN, pull=Pin.PULL_DOWN)
loadSCK = pin( , Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT)

def where_am_i():
    current_location = [enes100.x, enes100.y, enes100.theta]
    return current_location

def object_detect():
    distance = sensor.distance_cm()
    return distance #returns distance in CM

#one

def subtask_two(): #done (unused code)
    motor1.backward(25)
    motor2.formard(25)

def subtask_three(): #done (unused code)
    motor1.forward(25)
    motor2.formard(25)
    time.sleep(.125)
    motor1.stop()
    motor2.stop()
    time.sleep(.125)
    
    motor1.forward(25)
    motor2.formard(25)
    time.sleep(.125)
    motor1.stop()
    motor2.stop()
    time.sleep(.125)
    
    motor1.forward(25)
    motor2.formard(25)
    time.sleep(.125)
    motor1.stop()
    motor2.stop()
    time.sleep(.125)

def subtask_four(): #done (4 and 5)
    while 1:
        where_am_i()
        enes100.print(current_location)

def subtask_five(): #done (unused code)
    if enes100.is_connected:
        enes100.print("subtask 5, wireless transmit success!!")
        
    return

# six

# seven

def subtask_eight():
    while 1:
        object_detect()
        if distance > 0:
            if distance < 5:
                enes100.print("object within 5cm of sensor")
                
        print(distance)
        time.sleep(1)
        
def subtask_nine():
    
    hx711.tare()
    
    value = hx711.read()
    value = hx711.get_value()
        
# ten
    
subtask_nine()
    
