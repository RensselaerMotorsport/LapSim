"""1/2 Skid Pad"""

from classes.car_simple import Car
from helper_functions_ev.py import calc_vmax 

car = Car("data/rm26.json")

OR = 18.25
IR = 15.25

V_O = calc_vmax(OR, car)
V_I = calc_vmax(iR, car)

circum_O = 2*3.14*OR
cirum_I = 2*3.14*IR

print("Velocity Outer =", V_O)


