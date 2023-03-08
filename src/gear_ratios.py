import math
import numpy as np
import matplotlib.pyplot as plt
from helper_functions_ev import motor_torque
from helper_functions_ev import traction_force
from helper_functions_ev import braking_force
from classes.car_simple import Car
from acceleration import run_accel
import warnings

warnings.filterwarnings("ignore")
car = Car("data/rm26.json")


def plot_torque_rpm():
    x1 = []
    y1 = []
    maxRPM = 4500

    for i in range(1, maxRPM, 1):
        x1.append(i)
        y1.append(motor_torque(car, i, peak=False))

    fig, ax = plt.subplots(1)
    ax.plot(x1, y1, '-g')
    ax.set_ylim(ymin=0)
    ax.set_xlim(left=0)

    plt.title("Tractive Force", fontsize=18, y=1.04)
    plt.xlabel("Motor speed (RPM)", fontsize=12)
    plt.ylabel("Torque (Nm)", fontsize=12)
    ax.legend(["Continuous motor torque"])
    ax.grid()
    plt.show()


def calc_tractive_force(car, GR, v, vMax, peak=False):
    r = car.attrs["tire_radius"]
    V = []
    F = []
    while v <= vMax:
        V.append(v)
        F.append(motor_torque(car, v * 60 * GR / (2 * math.pi * r), peak=peak) * GR / r)
        v += 0.01
    return V, F


def calc_traction_force(car, v, vMax, mu):
    V = []
    F = []
    while v <= vMax:
        V.append(v)
        F.append(traction_force(car, v, mu))
        v += 0.01
    return V, F


def braking_length(car, v0, v1, mu=0, tstep=0.001, returnTime=False):
    if mu == 0: mu = car.attrs["CoF"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    v = v0
    t = 0
    d = 0
    while v > v1:
        d += v * tstep
        t += tstep
        v -= braking_force(car, v, mu) / m * tstep
    if returnTime:
        return t
    else:
        return d


def forward_int(car, v0, d1, GR=0, mu=0, tstep=0.001, peak=False):
    if mu == 0: mu = car.attrs["CoF"]
    if GR == 0: GR = car.attrs["final_drive"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    r = car.attrs["tire_radius"]
    if v0 == 0: v0 = 0.0001
    v = [v0]
    d = [0]
    t = [0]
    i = 0
    while d[i] < d1:
        RPM = 60 * v[i] / (2 * math.pi * r)
        a = min((motor_torque(car, RPM, peak=peak) * GR / (r), traction_force(car, v[i], mu))) / m
        v.append(v[i] + a * tstep)
        t.append(t[i] + tstep)
        d.append(d[i] + v[i] * tstep)
        i += 1
    return v, d


def brake_pos(car, v1, v, d, mu=0):
    # CURRENTLY BROKEN
    if mu == 0: mu = car.attrs["CoF"]
    for i in range(-len(v), -1):
        if braking_length(car, v[-i - 1], v1, mu=mu) <= d[len(d) - 1] - d[0]:
            return braking_length(car, v[-i - 1], v1, mu=mu), braking_length(car, v[-i - 1], v1, mu=mu, returnTime=True)
    raise ValueError


def find_time(d, bpos, tstep):
    # CURRENTLY BROKEN
    for i in range(len(d)):
        if bpos <= d[i] + 0.05 and bpos >= d[i] - 0.05:
            return i * tstep
    raise ValueError


def racing_segment_time(car, v0, v1, d1, GR=0, mu=0, peak=False, tstep=0.001):
    # CURRENTLY BROKEN
    if mu == 0: mu = car.attrs["CoF"]
    if GR == 0: GR = car.attrs["final_drive"]
    v, d = forward_int(car, v0, d1, GR=GR, mu=mu, peak=peak, tstep=tstep)
    bpos = brake_pos(car, v1, v, d, mu=mu)
    return bpos[1] + find_time(d, bpos[0], tstep)
    # print(racing_segment_time(car, 0, 99, 75))


def plot_tfd(car, GR, mu):
    vMax = 35
    v = 0.01

    Ptractive = calc_tractive_force(car, GR, v, vMax, peak=True)
    Ctractive = calc_tractive_force(car, GR, v, vMax)
    traction = calc_traction_force(car, v, vMax, mu)
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
    print("Accel time (s): " + str(run_accel(car, GR=GR, peak=True, mu=mu)))


display_specs(car, 38/12, mu=1.7)
#plot_accel(car, 2.5, 4, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], plotPoints=True, peak=True)
