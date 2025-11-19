# 11/12 - initial code designed to orient otv towards a value (tailored for theta = pi/2)
#
#
#
#
#
# ------------------- <Initialize Code> --------------------

import machine, time, math
from machine import Pin, PWM, ADC

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100
from dcmotor import DCMotor
from servo import Servo

#enes100.begin("matbot", "MATERIAL", 328, 1120)

sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 5000)

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

def get_weight(): #input theta in degrees for sanity of troubleshooting in mso2 function later.
    value = hx711.get_value() / -823 # -823 is a calibration value to convert the amplified data to grams.
    
    return value

# ------------------- </Initialize Code> --------------------

def nav2():
    motor1.backwards(50)
    motor2.forward(50)
    

def nav1(): # Navigate to withon 150mm of mission site.
    
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
                motor1.forward(5)
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
                motor2.backwards(5)
        
        return 1
    # --- / turn functions ---
    
    
    time.sleep(2)
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
        
        # drive down until y ~= 0.5
        while current_location[1] > (0.5 + 0.075): # 0.075M is half of the 150mm distance from mission site)
            where_am_i()
            
            #if current_location[2] > theta + 0.26:
            #    motor1.stop()
            #    motor2.stop()
            #    cw_turn(theta)
                
            #if current_location[2] < theta + 0.26:
            #    motor1.stop()
            #    motor2.stop()
            #    ccw_turn(theta)
                
            motor1.backward(5)
            motor2.forward(5)
            
            time.sleep(0.125)
            
        motor1.stop()
        motor2.stop()
        
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
            
        #drive up until y ~= 1.5
        while current_location[1] < (1.5 - 0.075): # 0.075M is half of the 150mm distance from mission site)
            where_am_i()
            
            #if current_location[2] > theta + 0.26:
            #    motor1.stop()
            #    motor2.stop()
            #    cw_turn(theta)
                
            #if current_location[2] < theta + 0.26:
            #    motor1.stop()
            #    motor2.stop()
            #    ccw_turn(theta)
                
            motor1.backward(5)
            motor2.forward(5)
            
            time.sleep(0.125)

        motor1.stop()
        motor2.stop()
    
    # def nav_site(): ?
    # brainstorm:
    #
    # drive to within half distance, then "scan" for the block using rear mounted vision system?
    # block side/corner detection?
    #

def mso1():
    print("squish + transmit")
    
    claw_servo.write(70)
    #lift_servo.write(90) # lift not working
    
    time.sleep(5)
    
    #material - as soon as we squeeze we will know if it is plastic or foam
    
    claw_servo.write(40)
    
    time.sleep(4)
    
    old_angle = angle_detect()
    
    #print(old_angle)
    
    claw_servo.write(30)
    
    time.sleep(4)
    
    #print(angle_detect()) #will read around 1936 for plastic, 1836 for foam
    
    if angle_detect() < 1900:
        enes100.mission('MATERIAL_TYPE', 'FOAM')
    else:
        enes100.mission('MATERIAL_TYPE', 'PLASTIC')
    
    #lift - get the servo to squeeze and lift
    
    #weight - use load cell
    
def mso2():
    print("weight + transmit")
    
    # Ball masses ±20 g: 105 g, 190 g, 275 g
    # Cutoffs, 80g < m < 148g, 148g < m < 233g, 233g < m < 300g

    lift_servo.write(75) #15 degrees above horizontal
    claw_servo.write(70)
    
    time.sleep(2)
    
    claw_servo.write(35)
    
    time.sleep(2)
    
    lift_servo.write(60)
    
    time.sleep(2)

    while 1:   
        print(hx711.get_value() / -823)
        time.sleep(.125)
    
def mso3():
    print("mso3 - lift")
    
    lift_servo.write(0)
    
    time.sleep(2)
    
    lift_servo.write(90)
    
nav2()
# mso1()
