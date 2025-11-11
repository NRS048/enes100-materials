import machine, time
from machine import Pin, PWM

from hcsr04 import HCSR04
from hx711_gpio import HX711
from time import sleep
from enes100 import enes100
from dcmotor import DCMotor

enes100.begin("matbot", "MATERIAL", 328, 1120)#1120 normal, 1116 aux

sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 10000)

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

hx711 = HX711(loadSCK, loadOUT)

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

def subtask_six():
    
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
    
    time.sleep(2)
    current_location = where_am_i()
    print(current_location)
    
    if (current_location[2] < 1.83 and current_location[2] > 1.31):
        enes100.print("go")
        enes100.print(current_location[2])
        
    elif (current_location[2] < 1.32 and current_location[2] > 0):
        enes100.print("q1")
        enes100.print(current_location[2])
        ccw_turn(math.pi/2)
        
    elif (current_location[2] < 3.14 and current_location[2] > 1.82):
        enes100.print("q2")
        enes100.print(current_location[2])
        cw_turn(math.pi/2)
        
    elif (current_location[2] < -1.57 and current_location[2] > -3.14):
        enes100.print("q3")
        enes100.print(current_location[2])
        cw_turn(math.pi/2)
        
    elif (current_location[2] < 0 and current_location[2] > -1.58):
        enes100.print("q4")
        enes100.print(current_location[2])
        cw_turn(math.pi/2)
        
    enes100.print("facing right direction?")
    
    #while current_location[0] < 3.5:
    #    if current_location[1] < 1.5:
    #        enes100.print("y good")
    #    else:
    #        enes100.print("y bad")
        

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
    while 1:
        value = hx711.get_value()
        print(value/-823) #calibration value.
        time.sleep(.125)
            
# ten
    
subtask_six()
    
