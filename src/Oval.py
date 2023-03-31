"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import line_segment_time
from helper_functions_ev import calc_max_entry_v_for_brake
from helper_functions_ev import braking_length
from classes.car_simple import Car
from skidpad import skidpad
import numpy as np
import math



#Import Car Object
Car = Car("C:/Users/hlaval/Desktop/Lapsim Code/LapSim/src/data/rm26.json")

#Set Parameters for track 
straight_d = 77  #Range 61-77
corner_r = 15    #Range 15-25
n = (straight_d*2)+2  #number of segments

#Track is a two element array that stores the distance of a segment in the first column and its radius in the second
track = np.zeros((n+1,2))

#Create Track Using Parameters
for i in range(n):
    track[i,0] = straight_d/straight_d
#print(track)

#Add Corners for the Oval 
track[straight_d+1,1] = corner_r
track[straight_d+1,0] = 2*math.pi*corner_r
track[(straight_d*2)+1,1] = corner_r
track[(straight_d*2)+1,0] = 2*math.pi*corner_r
track[n,0] = 0
track[n,1] = 0
#print(track)


def runtrack(Car, track):
    """
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    Car - car object
    track - 2-D array of distance and radius

    Return - Track Time
    """
    #Initialize time and velocity arrays, time will be output and velocity can be conditional output (In future)
    time = np.zeros(track.size)
    velocity = np.zeros(track.size)
    velocity[0] = .0001

    u = np.zeros(track.size)

    
    for i in range(track.size):
        iter = i+1
        if iter == n:
            break

        #print("Iter =",iter)
        #print("Velocity =",velocity[i])
        #print("Radius =",track[i,1])
        #print("Distance=",track[i,0])

        if i > 0 and i < n-1:
            u[i] = calc_max_entry_v_for_brake(Car, velocity[i+1], track[i+1,1], track[i+1,0])
        if track[i,1] == 0:
            time[i+1],velocity[i+1] = line_segment_time(Car,track[i,0], velocity[i], timestep=.001) #velocity[i+1] is the exit velocity
        else:
            vmax = calc_vmax(corner_r,Car)
            #print("Vmax=", vmax)
            if velocity[i] < vmax or velocity[i] == vmax:
                time[i+1] = (math.pi*corner_r)/velocity[i]
                velocity[i+1] = velocity[i]
            else: #velocity > vmax
                for j in range(1,77):
                    d = braking_length(Car,velocity(-j),vmax,returnVal=1)
                    if abs(d - 77-j) < 1:
                        velocity[j:] = braking_length(Car,velocity(-j),vmax,returnVal=2)
                        time[j:] = braking_length(Car,velocity(-j),vmax,returnVal=3)



    return ("Lap Time is", np.sum(time, axis=None))

#print(runtrack(Car, track))


#plt.plot(forward_int(Car, 0,27,returnVal=0),forward_int(Car, 0,27,returnVal=1))
#plt.show

