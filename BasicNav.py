# 11/12 - initial code designed to orient otv towards a value (tailored for theta = pi/2)
#
#
#
#
#
# ------------------- <Initialize Code> --------------------

import machine, time
from machine import Pin, PWM

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100
from dcmotor import DCMotor

enes100.begin("matbot", "MATERIAL", 328, 1120)

#sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 5000)

Pin1 = Pin(12, Pin.OUT)
Pin2 = Pin(13, Pin.OUT)
enable1 = PWM(Pin(14), 15000)

Pin3 = Pin(25, Pin.OUT)
Pin4 = Pin(26, Pin.OUT)
enable2 = PWM(Pin(27), 15000)

motor1 = DCMotor(Pin1, Pin2, enable1)
motor2 = DCMotor(Pin3, Pin4, enable2)

loadOUT = Pin(32, Pin.IN, pull=Pin.PULL_DOWN)
loadSCK = Pin(33, Pin.OUT)

#hx711 = HX711(loadSCK, loadOUT)

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

# ------------------- </Initialize Code> --------------------

def nav1():
    
    #  --- turn functions ---
    def cw_turn(theta):
        while 1:
            current_location = [enes100.x, enes100.y, enes100.theta]
            if current_location[2] < theta + 0.26: # < 1.83
                if  current_location[2] > theta - 0.26: #> 0.31
                    enes100.print("winner")
                    motor2.stop()
                    break
            else:
                #enes100.print("not at goal yet!")
                #enes100.print(current_location[2])
                #time.sleep(1)
                #motor1.forward(5)
                motor2.forward(5)
            
        return 1
        
    def ccw_turn(theta):
        while 1:
            if enes100.theta > theta - 0.26:
                if enes100.theta < theta + 0.26:
                    #print("winner")
                    motor1.stop()
                    break
            else:
                #print("not at goal yet!")
                #time.sleep(1)
                motor1.backwards(5)
        
        return 1
    # --- / turn functions ---
    
    
    time.sleep(2)s
    current_location = where_am_i()
    print(current_location)
    
    if current_location[0] is None:
        print("lost")
        return
        
        
    #NEW Nav developing below
        
    #math.pi/12 = 0.26 in these cases
    #math.pi/2 = 1.57
    #3*math.pi/4 = 4.71
        
    if current_location[1] > 1:
        theta = math.pi / 2
        
        print ("top")
        
        if (current_location[2] > (theta - 0.26) and current_location[2] < (theta + 0.26)):
            print("correct orientation")
            
        elif (current_location[2] > (theta + 0.26) and current_location[2] < 4.71 ):
            print("cw_turn")
            cw_turn(theta)
            
        else:
            print("ccw_turn")
            ccw_turn(theta)

        
    elif current_location[1] < 1:
        theta = 3 * math.pi / 2
        
        print ("bottom")
            
        if (current_location[2] > (theta - 0.26) and current_location[2] < (theta + 0.26)):
            print("correct orientation")
            
        elif (current_location[2] < (theta - 0.26) and current_location[2] > 1.57 ):
            print("ccw_turn")
            ccw_turn(theta)
            
        else:
            print("cw_turn")
            cw_turn(theta)
    
    # def nav_site(): ?
    # brainstorm:
    #
    # drive to within half distance, then "scan" for the block using rear mounted vision system?
    # block side/corner detection?
    #
    
def mso1():
    print("mso1 - weigh/transmit")
    
def mso2():
    print("mso2 - squish/transmit")
    
def mso3():
    print("mso3 - something")
    
nav1()
