import math

enes100.begin("matbot", "MATERIAL", "arcoID", 1120)

location_last = [0, 0, 0]

wheel_diameter = 60 #60 mm

wheel_circumference = 60 * math.pi # 188.50mm

wheelbase_circumference = 258 * math.pi # distance from center to inside edge of wheel

motor_rpm = 450

def find_location():
    if enes100.visible:
        location_last = [enes100.x, enes100.y, enes100.theta]
        return 1 # (OTV visible and data saved)
    else:
        return 0 # (OTV not visible to arena)
    
def point_direction(current_theta, desired_theta, desired_speed):
    
    
    delta_theta = desired_theta - current_theta # find angle between the two theta values
    arc_portion = delta_theta / math.pi
    time_on = ((arc_portion * wheelbase_circumference) / wheel_circumference) / (3 * desired_speed /40)
    #use the desired_speed variable here, and for the h-bridge communication
    
    
    
find_location()

#Sub-Task 1: Follow the rules

#Sub-Task 2: Forward locomotion
def subtask_two():
    if find_location() = 0:

    