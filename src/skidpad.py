"""A module to calculate the velocities and time for a Skid Pad"""

from classes.car_simple import Car
from helper_functions_ev import calc_vmax 

car = Car("C:/Users/hlaval/Desktop/Lapsim Code/LapSim/src/data/rm26.json")


### Below is a troubleshooting script ###

OR = 18.25   #Outer radius
IR = 15.25   #Inner radius
Mid = 16.75  #Middle radius

V_O = calc_vmax(OR, car)
V_I = calc_vmax(IR, car)
V_M = calc_vmax(Mid,car)

circum_O = 2*3.14*OR
circum_I = 2*3.14*IR
circum_M = 2*3.14*Mid

print("Velocity Outer =", V_O)
print("Velocity Inner =", V_I)
print("Velocity Middle =", V_M)


t_O = circum_O/V_O
t_I = circum_I/V_I
t_M = circum_M/V_M

print("Time Outer =",t_O)
print("Time_Inner =",t_I)
print("Time_Middle =",t_M)

#This model will likely predict a slower skidpad time than in real life because the tire model is basically non existent.



def skidpad(r, car):
    """
    A function that inputs a json (eventually) and outputs time and other things maybe
    """
    v = calc_vmax(r,car)
    circum = 2*3.24*r
    t = circum/v

    return t

