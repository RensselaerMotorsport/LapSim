"""Acceleration event calculation."""

#import math
#from helper_functions_ev.py import calc_vmax
from classes.car_simple import Car
from helper_functions_ev import straightlinesegmenttime

car = Car("data/rm26.json")

def run_accel(car):
    return straightlinesegmenttime(car, 75, vinitial= 0.001)

print(run_accel(car))
