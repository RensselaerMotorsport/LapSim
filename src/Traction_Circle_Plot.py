"""A module to plot the traction circle of each tire"""

import numpy as np
import math 
from math import pi
from Weight_Transfer import calc_total_weight_transfer
from Weight_Transfer import add_aero_loads
from matplotlib import pyplot as plt

m = 295 #total mass of car+driver
mew = 1.6 #coef of friction

def calc_lat_accel(v, icr):
    """
    Calculates lateral acceleration

    Imputs:
    v - velocity in m/s
    icr - inverse corner radius in rad

    Output:
    Lateral acceleration in m/s**2
    """
    return (m*(v**2))/icr


def calc_t(v1, v2, d_step):
    """
    Calculates the time it takes to complete segment n

    Inputs:
    v1 - velocity at the begining of segment n
    v2 - velocity at the end of segment n
    d_step - distance step

    Output:
    t - time in s
    """
    return 1/(((v1+v2)/2)/d_step)


#not sure how we should distinguish the difference between long and lat velocities
#good thing is we know all long accel is caused by engine force and any lat accel is caused by curavture

def calc_long_accel(v1, v2, t):
    """
    Calculates longitudinal acceleration

    Inputs:
    v1 - velocity at the begining of segment n
    v2 - velocity at the end of segment n
    t - the time it takes to complete segment n

    Output:
    Longitudinal acceleration
    """

    return (v1+v2)/t
    #yes?


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


def plot_friction_circle(ax, ay, v, t_no):
    """
    Plots the tire friction circle (elipse)

    Inputs:
    ax - longitudinal acceleration
    ay - lateral acceleration
    v - velocity 
    t_no - tire number

    Output:
    Plot of tire friction circle
    """

    u=0    #x-position of the center
    v=0    #y-position of the center
    total_Fn = calc_total_Fn(ax,ay,v,t_no)

    a = np.zeros(4)
    for i in range(1,4):
        a[i] = add_aero_loads(v,i)
    total_aero_loads = np.sum(a)
    
    result_y = ay*m
    result_x = ax*m
    smol_resultant_y = result_y*((total_Fn)/(total_aero_loads+np.sum(Steady_weight)))
    smol_resultant_x = result_x*((total_Fn)/(total_aero_loads+np.sum(Steady_weight)))


    t = np.linspace(0, 2*pi, 100)

    lat= mew*total_Fn   #radius on the x-axis
    long= mew*total_Fn  #radius on the y-axis
    plt.title("Friction Circle of Tire {}".format(t_no))
    plt.xlabel("Lateral Force (N)")
    plt.ylabel("Longitudinal Force (N)")
    plt.plot(u+lat*np.cos(t) , v+long*np.sin(t) )
    plt.arrow(0,0,smol_resultant_x,smol_resultant_y, width=10)
    plt.grid(color='lightgray',linestyle='--')
    plt.show()
    print(total_Fn,"Newtons")


def plot_vehicle_friction_plot(ax, ay, v):
    """
    Plots the vehicle friction circle 
    
    Inputs:
    ax - longitudinal acceleration
    ay - lateral acceleration
    v - velocity 


    Output:
    Plot of total vehicle friction circle
    """

    
    plt.title("Friction Circle of Vehicle")
    plt.xlabel("Lateral Force (N)")
    plt.ylabel("Longitudinal Force (N)")
    plt.plot(u+lat*np.cos(t) , v+long*np.sin(t) )
    plt.arrow(0,0,smol_resultant_x,smol_resultant_y, width=10)
    plt.grid(color='lightgray',linestyle='--')
    plt.show()
    