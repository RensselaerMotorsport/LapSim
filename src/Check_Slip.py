"""A module to find if wheels slip"""

import numpy as np
import Weight_Transfer as wt
import helper_functions as h
import Traction_Circle_Plot as tc

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
        return (Steady_weight[0]+wt.calc_total_weight_transfer(ax, ay, v, t_no))*Cf

    elif t_no == 2:
        return (Steady_weight[1]+wt.calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    
    elif t_no == 3:
        return (Steady_weight[2]+wt.calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    
    elif t_no == 4:
        return (Steady_weight[3]+wt.calc_total_weight_transfer(ax, ay, v, t_no))*Cf
    else:
        raise ValueError; 't_no must be 1,2,3, or 4'



wheel_effective_radius = .2032
tranny_efficiency = .9



# available_engine_force = (torque_at_wheels * tranny_efficiency)/wheel_effective_radius
# throttle_pos = 1 #any number between 0-1, 1 is max throttle
# throttle = available_engine_force*throttle_pos


# torque to driven wheel is given by the same excel files that give torque for a given gear
# if torque force to driven wheels is greater than friction force decrease throttle (slip occurs)
# only need to check driven wheels (rear)
# if slip occurs, decrease throttle by some factor and restart the segment


def check_torque_for_slipping(car, torque,d_step=.1, v1=0.001, gear=1, transmissionefficency=.9, tireschecked=np.matrix[3,4]):
    """"
    Checks a provided torque to see if it causes the car to slip.
    
    Given: car, the car object we are testing
    torque, the torque we are testing
    d_step, the distance between each step, default is .1 m
    v1, the initial velocity of the car while checking this torque, default is stationary .001
    gear, the gear the car is in, default is 1
    transmissionefficency, the efficency of the transmission in the car, default is .9
    tires checked, a numpy matrix of the tire numbers we are checked, default is [3,4]
    
    Returns: True or False output, True if the car is slipping, False if it is 

    Note:
    Modeling traction like this could potentially cause incorrect results for modelling acceleration from
    slow corners with increasing radius. If we would like to improve the model the amount of centripetal 
    force required at the same time will need to be taken into account. This would add a velocity component orthogonal to the 
    tangential component decreasing traction. Thus our model overestimates the traction our tires have. 
    
    """
    wheeltorque=h.calc_torque_at_wheels(gear, torque, car, transmissionefficency)
    engineforce=h.calculate_engine_force(car, wheeltorque,transmissionefficency)
    dragforce=h.calculate_drag_force(car,v1)
    v2=h.calculate_velocity_new(engineforce,dragforce,car,v1,step=1)
    t=h.calc_t(v1,v2,d_step)
    longaccel=h.calc_long_accel(v1,v2,t)
    tangentialforceatwheel=h.get_tangent_force_at_wheels(gear,torque,car)
    for i in range(np.shape(tireschecked)):
        frictionforce=calc_friction_force(tireschecked[i],longaccel,v1)
        if frictionforce<tangentialforceatwheel:
            return True
    return False

