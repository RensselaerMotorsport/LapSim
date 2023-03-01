import matplotlib.pyplot as plt
from classes.car_simple import Car
from helper_functions_ev import motor_torque
import math
car = Car("data/rm26.json")

def plot_traction_force(car, maxv=100/3.6, step=0.01):
    from check_slip import calc_friction_force
    v = step
    ax = step
    F = []
    V = []
    while v < maxv:
        ax = calc_friction_force(2, ax, v)
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

def plot_tractive_force(car, gear=3.5, maxv=200/3.6, step=1):
    RPM = step
    V = []
    F = []
    while RPM * 2 * math.pi * car.attrs["tire_radius"] / (60 * gear) < maxv:
        V.append(RPM * 2 * math.pi * car.attrs["tire_radius"] * 3.6 / (60 * gear))
        F.append(motor_torque(car, RPM, peak=True))
        RPM += step
    plt.title("Tractive Force Diagram")
    plt.xlabel("Velocity (km/hr)")
    plt.ylabel("Tractive Force (N)")
    plt.plot(V, F)
    plt.show()

plot_tractive_force(car)