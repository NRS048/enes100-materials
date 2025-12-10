#new ms7 because the origional one sucks

# ------------------- <Initialize Code> --------------------

import machine, time, math
from machine import Pin, PWM, ADC

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100 
from dcmotor import DCMotor
from servo import Servo

#enes100.begin("matbot", "MATERIAL", 328, 1120) # vision system setup

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

claw_servo = Servo(pin_id=16) #replaced with code in mso2
lift_servo = Servo(pin_id=23)

claw_servo.write(70) #use 40 for grab, 70 for open
lift_servo.write(75) #prelift claw

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

hx711 = HX711(loadSCK, loadOUT)
hx711.tare() # skip this?

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

def get_weight(): #input theta in degrees for sanity of troubleshooting in mso2 function later.
    value = hx711.get_value() / -823 # -823 is a calibration value to convert the amplified data to grams. Needs recalibration & verification for during lift.
    
    return value

# ------------------- </Initialize Code> --------------------

#def cwturn(theta):
#   while True:
#        motor1.forward(2)
#        
#        oldtime = time.time()
#        
#        while time.time() - oldtime < .0625: # makeshift time.sleep(s) function
#                continue
#            
#        motor1.stop()
#        motor2.stop()
#        current_location = where_am_i()
#        time.sleep(.25)
#        
#        if (current_location[2] < theta + 0.26) and (current_location[2] > theta - 0.26):
#            enes100.print("break")
#            break
#        
#    enes100.print("good")

# ------------------ mission objectives ------------------ 

#enes100.print("squish + transmit")
    
claw_servo.write(70)
lift_servo.write(90)

time.sleep(3)

claw_servo.write(40)

time.sleep(4)

old_angle = angle_detect()

enes100.print(old_angle)

time.sleep(0.5)

claw_servo.write(30)

time.sleep(2)

enes100.print(angle_detect())

new_angle = angle_detect()

print(old_angle)
print(new_angle)

if old_angle - new_angle > 80: # old_angle - angle_detect() to find "delta squish" and compare for both plastic and foam #122 for foam # 51 for plastic
    #enes100.mission('MATERIAL_TYPE', 'FOAM')
    print("foam")
else:
    #enes100.mission('MATERIAL_TYPE', 'PLASTIC')
    print("plastic")

lift_servo.write(60)

time.sleep(2)

weight = (hx711.get_value() * 175.1/-35475.458) + 9.5

#enes100.print(weight)
print(weight)

if weight > 300: #231
    #enes100.mission('WEIGHT', 'HEAVY')
    print("Heavy")
elif weight > 150: #143.5
    #enes100.mission('WEIGHT', 'MEDIUM')
    print("Medium")
else:
    #enes100.mission('WEIGHT', 'LIGHT')
    print("Light")
    
