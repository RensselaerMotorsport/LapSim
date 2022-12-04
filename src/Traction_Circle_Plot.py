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

def calc_slip_angle(icr, b, a, v_long, v_lat):
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

    t_no_slip_angle = np.zeros(3)
    t_no_slip_angle[0] = (180-A) - (a/A) - (v_long/v_lat)
    t_no_slip_angle[1] = (180-A) - (a/A) - (v_long/v_lat)
    t_no_slip_angle[2] = (b/A) - (v_long/v_lat)
    t_no_slip_angle[3] = (b/A) - (v_long/v_lat)

    return t_no_slip_angle


def plot_friction_circle(ax, ay, v_lat, v_long, icr, t_no):
    """
    Plots the tire friction circle (elipse)

    Inputs:
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

    slip_ang = calc_slip_angle(icr, v_long, v_lat, b=2, a=2) #####!!!!! need to use object car with this function and this application of it for b and a parameters

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
    plt.text(2700, 5000, "Wheel slip angle=")
    plt.text(5000,5000, slip_ang[t_no])
    plt.show()
    print(Fn_tire,"Newtons")


def plot_vehicle_friction_plot(ax, ay, v_lat, v_long):
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
    wheel= math.atan(v_lat/v_long)

    plt.title("Friction Circle of Vehicle")
    plt.xlabel("Lateral Force (N)")
    plt.ylabel("Longitudinal Force (N)")
    plt.plot(x+lat*np.cos(t) , y+long*np.sin(t) )
    plt.arrow(0,0,result_x,result_y, width=70)
    plt.text(2700, 5000, "Vehicle slip angle=")
    plt.text(5000,5000, wheel)
    plt.grid(color='lightgray',linestyle='--')
    plt.show()
    
plot_vehicle_friction_plot(10,7,12)