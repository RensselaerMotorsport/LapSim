"""A module to plot the traction circle of each tire"""

import numpy as np
import math 
from math import pi
from Weight_Transfer import calc_total_weight_transfer
from Weight_Transfer import add_aero_loads
from matplotlib import pyplot as plt
import helper_functions as h
# from classes.car_simple import Car
# car = Car("data/rm26.json")

m = 295 #total mass of car+driver
mew = 1.6 #coef of 


Steady_weight = np.array([353.63, 298.12, 591.61, 569.37]) #array of steady state tire loads with entry [0] equal to tire number 1

def calc_total_Fn(ax, ay, v, t_no):
    """
    Inputs:
    ax - longitudinal acceleration
    ay - lateral acceleration
    v - velocity 
    t_no = tire number

    Outputs:
    Total normal force on a given tire
    """
    return Steady_weight[t_no]+calc_total_weight_transfer(ax, ay, v, t_no)

def calc_slip_angle(icr, v_long, v_lat, b, a):
    """
    Caclulates the slip angles of all tires and ouputs them in an array with our tire number convention. 
    We can use coordinates and trig to find the angle between two sectors instead of the icr if needed.
    
    !!!(need to test the difference between using small angle aproximations and not for this function)!!!
    !!!(there is a lot of ways to calulate tire slip angle so this might need to be refined, this one is ackerman?)!!!


    Inputs:
    icr_n - Inverse corner radius of current sector
    b - distance from CG to rear axle
    a - distance from CG to front 
    v_long - longitudinal velocity
    v_lat - lateral velocity
    """
    A= 1/icr

    t_no_slip_angle = np.zeros(4)
    t_no_slip_angle[0] = (180-A) - (a/A) - (v_long/v_lat)
    t_no_slip_angle[1] = (180-A) - (a/A) - (v_long/v_lat)
    t_no_slip_angle[2] = (b/A) - (v_long/v_lat)
    t_no_slip_angle[3] = (b/A) - (v_long/v_lat)

    return t_no_slip_angle


def plot_friction_circle(car, ax, ay, v_lat, v_long, icr, t_no):
    """
    Plots the tire friction circle (elipse)

    Inputs:
    Car - car object
    ax - longitudinal acceleration
    ay - lateral acceleration
    v_lat - lateral velocity
    v_long - longitudinal velocity 
    icr - inverse corner radius
    t_no - tire number

    Output:
    Plot of tire friction circle
    """
    
    v = math.sqrt(v_lat**2 + v_long**2)

    slip_ang_r = calc_slip_angle(car, icr, v_long, v_lat, b=3, a=2) #####!!!!! need to use object car with this function and this application of it for b and a parameters
    slip_ang = np.round(slip_ang_r,5)

    x=0    #x-position of the center
    y=0    #y-position of the center
    Fn_tire = calc_total_Fn(ax,ay,v,t_no)

    a = np.zeros(3)
    for i in range(1,4):
        a[i-1] = calc_total_Fn(ax,ay,v,i)
    total_fn = np.sum(a)
    
    result_y = ay*m
    result_x = ax*m
    smol_resultant_y = result_y*((Fn_tire)/(total_fn))
    smol_resultant_x = result_x*((Fn_tire)/(total_fn))


    t = np.linspace(0, 2*pi, 100)

    lat= mew*Fn_tire   #radius on the x-axis
    long= mew*Fn_tire #radius on the y-axis
    plt.title("Friction Circle of Tire {}".format(t_no))
    plt.xlabel("Lateral Force (N)")
    plt.ylabel("Longitudinal Force (N)")
    plt.plot(x+lat*np.cos(t) , y+long*np.sin(t) )
    plt.arrow(0,0,smol_resultant_x,smol_resultant_y, width=10)
    plt.grid(color='lightgray',linestyle='--')
    plt.text(200, 1200, "Wheel slip angle=")
    plt.text(900,1200, slip_ang[t_no])
    plt.show()
    print(Fn_tire,"Newtons")


def plot_vehicle_friction(ax, ay, v_lat, v_long):
    """
    Plots the vehicle friction circle 
    
    Inputs:
    ax - longitudinal acceleration
    ay - lateral acceleration
    v_lat - lateral velocity
    v_long - longitudinal velocity 

    Output:
    Plot of total vehicle friction circle
    """
    
    v = math.sqrt(v_lat**2 + v_long**2)
    
    x = 0  #x-position of center
    y = 0  #y-position of center
    a = np.zeros(3)
    
    for i in range(1,4):
        a[i-1] = calc_total_Fn(ax, ay, v,i)
    total_Fn = np.sum(a)
    print(total_Fn)
    lat = mew*total_Fn
    long = mew*total_Fn
    t = np.linspace(0, 2*pi, 100)


    result_y = (ay*m)
    result_x = (ax*m)
    wheel= round(math.atan(v_lat/v_long), 5)

    plt.title("Friction Circle of Vehicle")
    plt.xlabel("Lateral Force (N)")
    plt.ylabel("Longitudinal Force (N)")
    plt.plot(x+lat*np.cos(t) , y+long*np.sin(t) )
    plt.arrow(0,0,result_x,result_y, width=70)
    plt.text(1300, 5500, "Vehicle slip angle=")
    plt.text(4500,5500, wheel)
    plt.grid(color='lightgray',linestyle='--')
    plt.show()
    
