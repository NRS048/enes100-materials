enes100.begin("MATBOT", "MATERIAL", "idk man", 1120) #check on arco marker ID

#enes100.x			#functions defined by the enes100 micropython library
#enes100.y
#enes100.theta
#enes100.is_visible

#enes100.print

#pseudocode

#when start:

#we will be placed randomly in one of two starting positions, in a random orientation.
#The objective will be place in the other zone. Zones are 0.9m seperate, and 0.55m
#from the wall.

#Step1

location_last = [0, 0 , 0]

def find_location():
    if enes100.visible:
        location_last = [enes100.x, enes100.y, enes100.theta]
    else:
        #get un-lost?
    
find_location() #need to find a way to account for lag. May need to test actual station first.

if location_last[0] > 0: #Find which starting location we are in. 
    #in the top lcoation?