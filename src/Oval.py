"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import line_segment_time
from classes.car_simple import Car
from skidpad import skidpad
import numpy as np

Car = Car("C:/Users/hlaval/Desktop/Lapsim Code/LapSim/src/data/rm26.json")


straight_d = 77  #Range 61-77
corner_r = 15 #Range 15-25

track = np.array()


def runtrack(Car, straight, corner):
    """
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    car - car object
    straight - straight distance
    corner  - corner radius
    """
    
    t1, v = line_segment_time(Car, straight)
    if v > calc_vmax(corner, Car):
        v = 
    print(v)
    t2 = skidpad(corner,Car)
    t3, vnew = line_segment_time(Car, straight, vinitial=v)
    print(vnew)
    vnew = calc_vmax(corner, Car)
    t4 = skidpad(corner, Car)

    t = t1 + t2 + t3 + t4

    return t


sol = runtrack(Car, straight_d, corner_r)
print(sol)


