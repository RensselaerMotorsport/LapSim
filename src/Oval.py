"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import straightlinesegmenttime
from classes.car_simple import Car
from skidpad import skidpad


straight_d = 77  #Range 61-77
corner_r = 15 #Range 15-25


def runtrack(car, straight, corner):
    """
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    car - car object
    straight - straight distance
    corner  - corner radius
    """
    
    t1, v = straightlinesegmenttime(car, straight)
    print(v)
    v = calc_vmax(corner_r, car)
    print(v)
    t2 = skidpad(corner_r,car)
    t3, vnew = straightlinesegmenttime(car, straight, vinitial=v)
    print(vnew)
    vnew = calc_vmax(corner_r, car)
    t4 = skidpad(corner_r, car)

    t = t1+ t2+ t3 +t4

    return t


print(runtrack(car, ))



