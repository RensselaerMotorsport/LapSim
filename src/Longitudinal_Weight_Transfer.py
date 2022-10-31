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

def calc_long_weight_transfer_1(ax):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration

    Outputs:
    weight_transfer_1 - weight transfer of tire 1
    """

    return -Cx1*W*(h/L)*(ax/g)

def calc_long_weight_transfer_2(ax):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration

    Outputs:
    weight_transfer_2 - weight transfer of tire 2
    """

    return -Cx2*W*(h/L)*(ax/g)

def calc_long_weight_transfer_3(ax):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration

    Outputs:
    weight_transfer_3 - weight transfer of tire 3
    """

    return Cx3*W*(h/L)*(ax/g)

def calc_long_weight_transfer_4(ax):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration

    Outputs:
    weight_transfer_4 - weight transfer of tire 4
    """

    return Cx4*W*(h/L)*(ax/g)


Cf = 1.6 #coef of friction

W1 = 353.63 #Weight on tire 1 in steady state
W2 = 398.12 #Weight on tire 2 in steady state
W3 = 591.61 #Weight on tire 3 in steady state
W4 = 569.37 #Weight on tire 4 in steady state

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
        return (W1+calc_long_weight_transfer_1(ax))*Cf

    if t_no == 2:
        return (W2+calc_long_weight_transfer_2(ax))*Cf
    
    if t_no == 3:
        return (W3+calc_long_weight_transfer_3(ax))*Cf
    
    if t_no == 4:
        return (W4+calc_long_weight_transfer_4(ax))*Cf



# torque to driven wheel is given by the same excel files that give torque for a given gear
# throttle is equal to the available engine force * the throttle position (between 0 and 1)
# available engine force = (torque at wheels * tranny efficiency (.9))/wheel effective radius (.2032)
# if torque force to driven wheels is greater than friction force decrease throttle (slip occurs)