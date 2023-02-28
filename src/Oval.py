"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import line_segment_time
from helper_functions_ev import calc_max_entry_v_for_brake
from classes.car_simple import Car
from skidpad import skidpad
import numpy as np
import math


Car = Car("C:/Users/hlaval/Desktop/Lapsim Code/LapSim/src/data/rm26.json")


straight_d = 77  #Range 61-77
corner_r = 15 #Range 15-25

n = (straight_d*2)+2  #number of segments
 
track = np.zeros((n,2))

for i in range(n):
    track[i,0] = straight_d/straight_d

#print(track)

track[straight_d+1,1] = corner_r
track[straight_d+1,0] = 2*math.pi*corner_r
track[(straight_d*2)+1,1] = corner_r
track[(straight_d*2)+1,0] = 2*math.pi*corner_r

#print(track)

# track = np.array([straight_d,0],
#                  [2*math.pi*corner_r,corner_r],
#                  [straight_d,0],
#                  [2*math.pi*corner_r,corner_r]) #2-D array, first entry is the distance step and the second is corner radius.


def runtrack(Car, track):
    """
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    car - car object
    track - 2-D array of distance and radius
    """
    time = np.zeros(track.size)
    velocity = np.zeros(track.size)
    velocity[0] = .0001

    u = np.zeros(track.size)

    for i in range(track.size):
        iter = i+1
        print("Iter =",iter)
        print("Velocity =",velocity[i])
        print("Radius =",track[i,1])
        print("Distance=",track[i,0])

        if i > 0:
            u[i+1] = calc_max_entry_v_for_brake(Car, velocity[i], track[i,1], track[i,0])
        if track[i,1] == 0:
            time[i+1],velocity[i+1] = line_segment_time(Car,track[i,0], velocity[i], timestep=.001) #velocity[i+1] is the exit velocity
        else:
            vmax = calc_vmax(corner_r,Car)
            print("Vmax=", vmax)
            if velocity[i] < vmax:
                time[i+1] = (math.pi*corner_r)/velocity[i]
                velocity[i+1] = velocity[i]
            if velocity[i] == vmax:
                time[i+1] = (math.pi*corner_r)/vmax
                velocity[i+1] = vmax
            else: #velocity > vmax
                for j in range(velocity[1],velocity[i]):
                    if velocity[j] < u[j]:
                        b = j                                #Equals the number of segments when braking must occur from the start of turn
                for k in range(i-(i-b)):
                    velocity[k-1] = u[k]
                    time[k-1] = 1/((velocity[k-1])/track[k-1,0])
                
    return np.sum(time)

print(runtrack(Car, track))