import math
import numpy as np
import matplotlib.pyplot as plt
from helper_functions_ev import motor_torque
from helper_functions_ev import traction_force
from classes.car_simple import Car
from acceleration import run_accel
import warnings

warnings.filterwarnings("ignore")
Car = Car("data/rm28.json")


def calc_tractive_force(car, gr, v, vmax):
    r = car.attrs["tire_radius"] #gets the tire radius of the car
    V = [] #sets the velocity array
    F = [] #Sets the tractive force array
    while v <= vmax: #Set up the loop over velocities
        V.append(v) #adds the current velocity to the velocity list
        F.append(motor_torque(car, v * 60 * gr / (2 * math.pi * r)) * gr / r) #calculates the tractive force using the motor torque function
        v += 0.01 #increases the velocity before the loop restarts
    return V, F


def calc_traction_force(car, v, vmax, mu):
    V = [] #sets the velocity array
    F = [] #sets the tractive force array
    while v <= vmax: #Set up the loop over velocities
        V.append(v) #adds the current velocity to the velocity array
        F.append(traction_force(car, v, mu)) #Calculates the traction force using the traction force function
        v += 0.01 #Increases the velocity before the loop restarts
    return V, F


def plot_tfd(car, gr, mu, metric=False):
    vmax = 35 #maximum velocity we are considering
    v = 0.01 #minimum velocity we are considering

    tractive = calc_tractive_force(car, gr, v, vmax)
    traction = calc_traction_force(car, v, vmax, mu)
    if metric:
        for i in tractive[0]: tractive[0][i] *= 2.237
        for i in traction[0]: traction[0][i] *= 2.237

        for i  in tractive[1]: i /= 4.448
        for i in traction[1]: i /= 4.448
    plt.plot(tractive[0], tractive[1], '-g')
    plt.plot(traction[0], traction[1], '-r')

    plt.ylim((0, 100 + max(max(traction[1]), max(tractive[1]))))
    plt.xlim((0, vmax))

    plt.title(str(round(gr, 3)) + " Gear Ratio", fontsize=18, y=1.04)
    if metric:
        plt.xlabel("Velocity (m/s)", fontsize=12)
        plt.ylabel("Force (N)", fontsize=12)
    else:
        plt.xlabel("Velocity (mph)", fontsize=12)
        plt.ylabel("Force (lbf)", fontsize=12)
    plt.legend(["Peak Tractive Force", "Traction Force (µ = " + str(mu) + ")"], loc="best")
    plt.grid()

    plt.show()


def plot_accel(car, LG, UG, mu, gStep=0.05, tmin=4.113, plotPoints=False):
    plt.figure(figsize=(9.6, 7.2))
    for j in mu:
        x = []
        y = []
        for i in np.arange(LG, UG + 2 * gStep, gStep):
            x.append(i)
            y.append(run_accel(car,gr=i, tmin=tmin, returnPoints=plotPoints, mu=j))
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


def display_specs(car, gr, mu=0.0):
    if mu == 0: mu = car.attrs["CoF"]
    plt.figure(figsize=(9.6, 7.2))
    voltage = car.attrs["max_voltage"]
    Kv = car.attrs["constant_kv"]
    r = car.attrs["tire_radius"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    g = 9.80665
    plot_tfd(car, gr, mu)
    print("Top speed (m/s): " + str(voltage * Kv * 2 * math.pi * r / (60 * gr)))
    print("Top speed (km/hr): " + str(voltage * Kv * 2 * math.pi * r * 3.6 / (60 * gr)))
    print("Top speed (mph): " + str(voltage * Kv * 2 * math.pi * r * 3.6 / (60 * 1.609 * gr)))
    print("Peak acceleration (g's): " + str(230 * gr / (r * m * g)))
    print("Accel time (s): " + str(run_accel(car, gr=gr, mu=mu, returnPoints=False)))

def display_wvs():
    x, y = traction = calc_traction_force(Car, 0.01, 35, 1.4)
    for i in range(len(y)):
        y[i] /= 1.4
    print(y[0])
    plt.plot(x, y)
    plt.title("Weight (N) vs. Speed (m/s)", fontsize=18, y=1.04)
    plt.grid()
    plt.show()

def plot_traction_force(car, maxv=100/3.6, step=0.01):
    v = step
    ax = step
    mu = car.attrs["CoF"]
    F = []
    V = []
    while v < maxv:
        calc_traction_force(car, v, maxv, mu)
        #while ax != calc_friction_force(2, ax, v):
        #    ax = calc_friction_force(2, ax, v)
        #    print(ax)
        V.append(v)
        F.append(ax * car.attrs["mass_car"])
        ax = step
        v += step

    plt.title("Traction Force Diagram")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Traction Force (N)")
    plt.plot(V, F)
    plt.show()

def plot_tractive_force(car, gear=3, maxv=200/3.6, step=1):
    RPM = step
    V = []
    F = []
    while RPM * 2 * math.pi * car.attrs["tire_radius"] / (60 * gear) < maxv:
        V.append(RPM * 2 * math.pi * car.attrs["tire_radius"] * 3.6 / (60 * gear))
        F.append(motor_torque(car, RPM))
        RPM += step
    plt.title("Tractive Force Diagram")
    plt.xlabel("Velocity (km/hr)")
    plt.ylabel("Tractive Force (N)")
    plt.plot(V, F)
    plt.show()

#display_specs(Car, 3.75, mu=1.4)
#plot_accel(Car, 2.5, 8, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], plotPoints=False)
#plot_accel(Car, 2.5, 8, [1.4], plotPoints=False)