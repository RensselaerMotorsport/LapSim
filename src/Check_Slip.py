"""A module to find if wheels slip"""

import numpy as np
from Weight_Transfer import calc_total_weight_transfer

g = 9.8 #m/s^2
mass_car = 195 #kg
mass_driver = 100 #kg
W = g*(mass_car+mass_driver) #N

Cf = 1.6 #coef of friction

Steady_weight = np.array([353.63, 298.12, 591.61, 569.37]) #array of steady state tire loads with entry [0] equal to tire number 1


def calc_friction_force(t_no, ax, v, ay=0):
    """
    Calculates friction force given the number tire and longitudinal acceleration
    
    Inputs:
    t_no - number tire
    ax - longitudinal acceleration
    v - velocity
    ay - lateral acceleration (defualt=0)

    Outputs:
    
    friction_force
    """

    if t_no == 1:
        return (Steady_weight[0]+calc_total_weight_transfer(ax, ay, v, t_no))*Cf

    elif t_no == 2:
        return (Steady_weight[1]+calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    
    elif t_no == 3:
        return (Steady_weight[2]+calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    
    elif t_no == 4:
        return (Steady_weight[3]+calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    else:
        raise ValueError; 't_no must be 1,2,3, or 4'



def calc_if_slip(t_no, ax, v, ay=0, torque):


    if t_no == 3
        if calc_friction_force > 


wheel_effective_radius = .2032
tranny_efficiency = .9



# available_engine_force = (torque_at_wheels * tranny_efficiency)/wheel_effective_radius
# throttle_pos = 1 #any number between 0-1, 1 is max throttle
# throttle = available_engine_force*throttle_pos


# torque to driven wheel is given by the same excel files that give torque for a given gear
# if torque force to driven wheels is greater than friction force decrease throttle (slip occurs)
# only need to check driven wheels (I think the front tires which is tire 1 and 2) 
# if slip occurs, decrease throttle by some factor and restart the segment



