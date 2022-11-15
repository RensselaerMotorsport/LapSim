"""Four Wheel Longitudinal Weight Transfer"""

####################### Neglects Aerodynamic Load Transfer #######################
 

import numpy as np

g = 9.8 #m/s^2
mass_car = 195 #kg
mass_driver = 100 #kg
W = g*(mass_car+mass_driver) #N

h = .323879 #COG height in m
L = 1.525 #m

y_ = .60137 #m
Y_ = .00737 #m

b_ = .92564 #m
B_ = .59936 #m

Tf = 1.228 #m
Tr = 1.188 #m

offset_ratio_F = (Y_*2)/(Tf/2)
offset_ratio_R = (Y_*2)/(Tr/2)

Cx1 = 1/2*(1-offset_ratio_F)
Cx2 = 1/2*(1+offset_ratio_F)
Cx3 = 1/2*(1-offset_ratio_R)
Cx4 = 1/2*(1+offset_ratio_R)

def calc_long_weight_transfer(ax, Cx):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration
    Cx - Weight transfer coef (also determines which tire load to calculate)

    Outputs:
    weight_transfer - weight transfer of tire
    """
    
    if Cx == Cx1 or Cx == Cx2:
        return -Cx*W*(h/L)*(ax/g)
    elif Cx == Cx3 or Cx == Cx4:
        return Cx*W*(h/L)*(ax/g) #means we are finding weight transfer for tire 3 or 4 (rear tires)
    else:
        raise ValueError; 'Cx must be equal to one of the four weight transfer coef'


Cf = 1.6 #coef of friction

Steady_weight = np.array([353.63, 298.12, 591.61, 569.37]) #array of steady state tire loads with entry [0] equal to tire number 1

def calc_friction_force(t_no,ax):
    """
    Calculates friction force given the number tire and longitudinal acceleration
    
    Inputs:
    t_no - number tire

    ax - longitudinal acceleration
    Outputs:
    
    friction_force
    """

    if t_no == 1:
        return (Steady_weight[0]+calc_long_weight_transfer(ax,Cx1))*Cf

    elif t_no == 2:
        return (Steady_weight[1]+calc_long_weight_transfer(ax,Cx2))*Cf
    
    elif t_no == 3:
        return (Steady_weight[2]+calc_long_weight_transfer(ax,Cx3))*Cf
    
    elif t_no == 4:
        return (Steady_weight[3]+calc_long_weight_transfer(ax, Cx4))*Cf
    else:
        raise ValueError; 't_no must be 1,2,3, or 4'


torque_at_wheels = np.array(1,2) #not actually, find these values from our csv files with torque for our lowest gear at lowest RPM (only for launch)
wheel_effective_radius = .2032
tranny_efficiency = .9

available_engine_force = (torque_at_wheels * tranny_efficiency)/wheel_effective_radius
throttle_pos = 1 #any number between 0-1, 1 is max throttle
throttle = available_engine_force*throttle_pos


# torque to driven wheel is given by the same excel files that give torque for a given gear
# if torque force to driven wheels is greater than friction force decrease throttle (slip occurs)
# only need to check driven wheels (I think the front tires which is tire 1 and 2) 
# if slip occurs, decrease throttle by some factor and restart the segment


