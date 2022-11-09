""""A module to plot the traction circle of each tire"""

import numpy as np
import math 
from math import pi
from Weight_Transfer import calc_total_weight_transfer
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


ax = 5
ay = 5
v = 5

u=0    #x-position of the center
v=0    #y-position of the center
lat= mew*calc_total_Fn(ax,ay,v,i)    #radius on the x-axis
long= mew*calc_total_Fn(ax,ay,v,i)  #radius on the y-axis

t = np.linspace(0, 2*pi, 100)
for i in range(3):
    plt.plot(u+lat*np.cos(t) , v+long*np.sin(t) )
    plt.grid(color='lightgray',linestyle='--')
    plt.show()



