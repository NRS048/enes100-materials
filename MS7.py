# MS7 Code in full - pseudo then real

# declare variables and basic functions

# START

# orient towards mission site

# navigate to within 150mm

# assuming dead-center block
# rotate 180 degrees - use vision system to check
# slowly drive straight until mission point, and a little extra to ensure depth

# assuming off-center block
# "sweep" using ultrasonic distance, find the relative location (coords?) of block
# orient and drive straight until you reach block, then continue to ensure depth

# squeeze - transmit material
# lift - trasmit weight

# drop cube and navigate to start of navigation section (backwards is forward, lead with ultrasonic)
# Check "top", if clear, continue, else move down to the next one.
# Check "top", if clear, continue to finish, else move down to next.
# navigate to finish and move through

# end code.

# ------------------- <Initialize Code> --------------------

import machine, time, math
from machine import Pin, PWM, ADC

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100 
from dcmotor import DCMotor
from servo import Servo

enes100.begin("matbot", "MATERIAL", 328, 1120) # vision system setup

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

def nav1(): # Navigate to within 150mm of mission site.
    
    #  --- turn function
    def turn(dtheta): 
        waittime = round((dtheta * 0.8), 2) #0.8 comes from solving 2.5s = 180 degrees
        
        enes100.print(dtheta)
        
        if waittime < 0:
            enes100.print("cw")
            motor1.forward(2)
            motor2.forward(2)
            
            oldtime = time.time()
            
            while time.time() - oldtime < abs(waittime): # makeshift time.sleep(s) function
                continue
            
            enes100.print("stop cw")
            motor1.stop()
            motor2.stop()
            #cw
            
        elif waittime > 0:
            enes100.print("ccw")
            motor1.backwards(2)
            motor2.backwards(2)
            
            oldtime = time.time()
            
            while time.time() - oldtime < abs(waittime):
                continue
            
            enes100.print("stop ccw")
            motor1.stop()
            motor2.stop()
            #ccw
            
    # --- / turn function ---
    
    
    time.sleep(2) # delay to ensure proper connection to vision system
    current_location = where_am_i()
    #print(current_location)
    
    if current_location[0] is None: # end run if not visible to vision system
        print("lost")
        return
        
        
    #NEW Nav developing below
        
    # math.pi / 12 = 0.26 in these cases
    # math.pi / 2 = 1.57
    # 3 * math.pi / 4 = 4.71
    # 2 * math.pi = 6.28
    def orient():
        if current_location[1] > 1: # top half of arena
            theta = 1.57 # goal direction, want to face straight up, drive down leading with sensor. ( math.pi / 2 )
            
            print ("top")
            
            if (current_location[2] > (theta - 0.26) and current_location[2] < (theta + 0.26)): # this will not happen. If our current orientation is correct (pointed towards block)
                print("correct orientation")
                
            elif (current_location[2] > (theta + 0.26) and current_location[2] < 4.71 ): # if we are facing somewhere in 2nd or 3rd quadrant of the unit circle
                print("cw_turn")
                dtheta = theta - current_location[2] # should be negative
                turn(dtheta)
                
            else: # if we are facing somewhere in the 1st of 4th quadrant of the unit circle.
                print("ccw_turn")
                if current_location[2] < 1.57: # quadrant one
                    dtheta = theta - current_location[2] # should be positive
                else: # quadrant four (seperate b/c the transfer from theta = 2pi to theta = 0 gets messy)
                    dtheta = theta + 6.28 - current_location[2] # should be positive
                
                turn(dtheta)
                
        elif current_location[1] < 1: # bottom half of arena
            theta = 4.71 # goal direction ( 3 * math.pi / 2) 
            
            print ("bottom")
                
            if (current_location[2] > (theta - 0.26) and current_location[2] < (theta + 0.26)): # This will not happen. If we are facing the correct way
                print("correct orientation")
                
            elif (current_location[2] < (theta - 0.26) and current_location[2] > 1.57 ): # if we are facing somewhere in the 2nd or 3rd quadrant
                print("ccw_turn")
                dtheta = theta - current_location[2] # should be positive
                turn(dtheta)
                
            else: # quadrants one and four 
                print("cw_turn") # if we are facing somewhere in the 1st or 4th quadrant
                if current_location[2] < 1.57: # quadrant one
                    dtheta = theta - current_location[2] - 6.28 # should be negative
                else: # quadrant four (seperate b/c the transfer from theta = 2pi to theta = 0 gets messy)
                    dtheta = theta - current_location[2]
                    
                turn(dtheta)
    orient()
    
    return
    
    current_location = where_am_i()
    
    if current_location[1] > 1: # top
        if not (current_location[2] < 1.57 + 0.26 and current_location[2] > 1.57 - 0.26):
            orient()
    else: # bottom
        if not (current_location[2] < 1.57 + 0.26 and current_location[2] > 1.57 - 0.26):
            orient()
        
nav1()