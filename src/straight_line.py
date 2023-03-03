from helper_functions import calculate_drag_force,\
    calculate_engine_force, \
    calculate_velocity_new, \
    calculate_friction_force, \
    get_tangent_force_at_wheels, \
    calc_rpm_given_speed

# from Check_Slip import calc_friction_force

from classes.car_simple import Car
import weight_transfer as wt

import pandas as pd

import matplotlib.pyplot as plt

import os

rpm_torque = pd.read_csv(r'C:\Users\barbot\Dropbox\PC\Documents\Projects\LapSim\src\data\emrax_torque.csv')

step = 0.1  # meters
initial_velocity = 0.01  # meters per second

car = Car("data/rm26.json") 

distance_travelled = 0
total_distance = 500  # meters

velocity = initial_velocity
current_gear = "1st"
trans_efficiency = 0.9
total_time = 0
velocities = []
steps = []
accels = []

# array of steady state tire loads with entry [0] equal to tire number 1
steady_weights = [353.63, 298.12, 591.61, 569.37]
Cf = car.attrs["CoF"]


def calc_friction_force(t_no, v, ay=0):
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
    dyn_p = wt.calc_dyn_p(v)
    A = 1
    Cl = 3
    downforce = Cl*dyn_p*A

    add_aero = downforce/4


    if t_no == 1:
        return (steady_weights[0] + add_aero) * Cf

    elif t_no == 2:
        return (steady_weights[1] + add_aero) * Cf

    elif t_no == 3:
        return (steady_weights[2] + add_aero) * Cf

    elif t_no == 4:
        return (steady_weights[3] +add_aero) * Cf


while distance_travelled < total_distance:
    initial_velocity = velocity
    distance_travelled += step

    rpm = calc_rpm_given_speed(1, velocity, car)
    max_torque = rpm_torque.loc[rpm_torque.rpm == round(rpm, -2), "torque"].reset_index(drop=True)[0]
    torque = max_torque

    wheel_torque = get_tangent_force_at_wheels(1, torque, car)
    drag_force = calculate_drag_force(car, velocity)
    engine_force = calculate_engine_force(car, wheel_torque, trans_efficiency)
    friction_force = calculate_friction_force(car, velocity)
    velocity = calculate_velocity_new(engine_force,
                                      drag_force, car,
                                      step, velocity)

    time = 1 / (((initial_velocity + velocity) / 2) / step)
    accel = (velocity - initial_velocity) / time

    rr = calc_friction_force(3, accel, velocity)
    rl = calc_friction_force(4, accel, velocity)

    # while rr < wheel_torque or rl < wheel_torque:
    #     torque -= 1
    #     # print(rr, rl, wheel_torque)
    #
    #     wheel_torque = get_tangent_force_at_wheels(1, torque, car)
    #     drag_force = calculate_drag_force(car, velocity)
    #     engine_force = calculate_engine_force(car, wheel_torque, trans_efficiency)
    #     friction_force = calculate_friction_force(car, velocity)
    #     velocity = calculate_velocity_new(engine_force,
    #                                       drag_force, car,
    #                                       step, velocity)
    #
    #     time = 1 / (((initial_velocity + velocity) / 2) / step)
    #     accel = (velocity - initial_velocity) / time
    #
    #     rr = calc_friction_force(3, accel, velocity)
    #     rl = calc_friction_force(4, accel, velocity)
    #
    # print("Torque: ", torque)
    # print("Velocity: ", velocity)
    total_time += time

    velocities.append(velocity)
    steps.append(distance_travelled)
    accels.append(accel)

print("Time: ", total_time)

plt.plot(steps, velocities, label="velocity (m/s")
plt.plot(steps, accels, label="acceleration (m/s^2)")
plt.xlabel("Distance travelled (m)")
plt.legend()
plt.show()
