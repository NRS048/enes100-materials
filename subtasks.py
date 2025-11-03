import time
from machine import Pin

from hcsr04 import HCSR04
from time import sleep
from enes100 import enes100

#enes100.begin(team_name: "matbot", team_type: "MATERIAL", aruco_id: 328, room_num: 1120)

sensor = HCSR04(trigger_pin = 19, echo_pin = 18, echo_timeout_us = 10000)

def object_detect():
    distance = sensor.distance_cm()
    return distance #returns distance in CM

#one

#two

#three

def subtask_four():
    current_location = [enes100.x, enes100.y, enes100.theta]
    return current_location

def subtask_five():
    if enes100.is_connected:
        enes100.print("subtask 5, wireless transmit success!!")
        
    return

#six

#seven

def subtask_eight():
    i = 1
    while i < 6:
        if object_detect() < 5:
            #enes100.print("object within 5cm of sensor")
            print("object within 5cm of sensor")
        i += 1
        time.sleep(1)
        
        
        
subtask_eight()
    
