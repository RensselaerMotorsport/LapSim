import math
import numpy as np
import matplotlib.pyplot as plt
from helper_functions_ev import motor_torque
from helper_functions_ev import traction_force
from classes.car_simple import Car
#from acceleration import run_accel
import warnings

warnings.filterwarnings("ignore")
car = Car("data/rm26.json")


def calc_tractive_force(car, GR, v, vMax, peak=False):
    """A function for calculating the tractive force along a series of velocities. 
    
    Given: car, the car object we are considering
    GR, the gear ratio
    v, the initial velocity we are considering
    vMax, the maxiumum velocity that you are considering
    peak, determines whether or not you want to use peak motor force, is a boolean, False means you do not, True means you want to use peak motor force
    
    Returns: V, a list of velocities
    F, a list of related tractive forces"""
    r = car.attrs["tire_radius"] #gets the tire radius of the car
    V = [] #sets the velocity array
    F = [] #Sets the tractive force array
    while v <= vMax: #Set up the loop over velocities
        V.append(v) #adds the current velocity to the velocity list
        F.append(motor_torque(car, v * 60 * GR / (2 * math.pi * r), peak=peak) * GR / r) #calculates the tractive force using the motor torque function
        v += 0.01 #increases the velocity before the loop restarts
    return V, F


def calc_traction_force(car, v, vMax, mu):
    """A function for calculating the traction force along a range of velocities.
    
    Given: car, the car object we are considering
    v, the initial velocity you are considering 
    vMax, the maximium velocity you are considering
    mu, the coefficent of friction
    
    Returns: V, the array of velocities considered
    F, the related Traction Forces"""
    V = [] #sets the velocity array
    F = [] #sets the tractive force array
    while v <= vMax: #Set up the loop over velocities
        V.append(v) #adds the current velocity to the velocity array
        F.append(traction_force(car, v, mu)) #Calculates the traction force using the traction force function
        v += 0.01 #Increases the velocity before the loop restarts
    return V, F


def plot_tfd(car, GR, mu):
    """Plots the tractive force diagram versus different velocities at a specified gear ratio and coefficent of friction.
    
    Given: car, the car object we are considering
    GR, the gear ratio we are considering
    mu, the coefficent of static friction we are considering
    
    Returns: A plot of the tractive force versus velocity at the specified gear ratio and coefficent of friction. Includes a plot of both peak and continuous torque as well as traction force
    Tractive force is what the motor can output, traction force is what the car can handle in real space, what the traction ability of the car is"""
    vMax = 35 #maximum velocity we are considering
    v = 0.01 #minimum velocity we are considering

    Ptractive = calc_tractive_force(car, GR, v, vMax, peak=True) #tractive force at peak torque
    Ctractive = calc_tractive_force(car, GR, v, vMax) #tractive force at continuous torque
    traction = calc_traction_force(car, v, vMax, mu) #traction force
    plt.plot(Ptractive[0], Ptractive[1], '-g')
    plt.plot(Ctractive[0], Ctractive[1], '-b')
    plt.plot(traction[0], traction[1], '-r')

    plt.ylim((0, 100 + max(max(traction[1]), max(Ptractive[1]))))
    plt.xlim((0, vMax))

    plt.title(str(round(GR, 3)) + " Gear Ratio", fontsize=18, y=1.04)
    plt.xlabel("Velocity (m/s)", fontsize=12)
    plt.ylabel("Force (N)", fontsize=12)
    plt.legend(["Peak Tractive Force", "Continuous Tractive Force", "Traction Force (µ = " + str(mu) + ")"], loc="best")
    plt.grid()

    plt.show()


def plot_accel(car, LG, UG, mu, gStep=0.05, tmin=4.113, plotPoints=False, peak=False):
    plt.figure(figsize=(9.6, 7.2))
    for j in mu:
        x = []
        y = []
        for i in np.arange(LG, UG + 2 * gStep, gStep):
            x.append(i)
            y.append(run_accel(car, GR=i, tmin=tmin, returnPoints=plotPoints, peak=peak, mu=j))
        plt.plot(x, y)

    plt.xlim((LG, UG))

    if plotPoints:
        plt.title("Acceleration event scores", fontsize=18, y=1.04)
    else:
        plt.title("Acceleration times (s)", fontsize=18, y=1.04)
    plt.xlabel("Gear Ratio", fontsize=12)
    if plotPoints == False:
        plt.ylabel("Time (s)", fontsize=12)
    else:
        plt.ylabel("Points", fontsize=12)
    leg = []
    for i in mu: leg.append("µ = " + str(i))
    plt.legend(leg, loc="best")
    plt.grid()
    plt.show()


def display_specs(car, GR, mu=0):
    if mu == 0: mu = car.attrs["CoF"]
    plt.figure(figsize=(9.6, 7.2))
    voltage = car.attrs["max_voltage"]
    Kv = car.attrs["constant_kv"]
    r = car.attrs["tire_radius"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    g = 9.80665
    plot_tfd(car, GR, mu)
    print("Top speed (m/s): " + str(voltage * Kv * 2 * math.pi * r / (60 * GR)))
    print("Top speed (km/hr): " + str(voltage * Kv * 2 * math.pi * r * 3.6 / (60 * GR)))
    print("Top speed (mph): " + str(voltage * Kv * 2 * math.pi * r * 3.6 / (60 * 1.609 * GR)))
    print("Peak acceleration (g's): " + str(230 * GR / (r * m * g)))
    print("Accel time (s): " + str(run_accel(car, GR=GR, peak=True, mu=mu, returnPoints=False)))

def display_wvs():
    x, y = traction = calc_traction_force(car, 0.01, 35, 1.4)
    for i in range(len(y)):
        y[i] /= 1.4
    print(y[0])
    plt.plot(x, y)
    plt.title("Weight (N) vs. Speed (m/s)", fontsize=18, y=1.04)
    plt.grid()
    plt.show()

#display_specs(car, 33/12, mu=1.4)
#plot_accel(car, 2.5, 4, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], plotPoints=False, peak=False)

