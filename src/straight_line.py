from helper_functions import calculate_drag_force,\
    calculate_engine_force, \
    calculate_velocity_new, \
    calculate_friction_force, \
    get_tangent_force_at_wheels, \
    calc_rpm_given_speed

from classes.car_simple import Car

import pandas as pd

rpm_torque = pd.read_csv("./data/emrax_torque.csv")

step = 0.1  # meters
initial_velocity = 0.01  # meters per second

car = Car("data/rm26.json")

distance_travelled = 0
total_distance = 75  # meters

velocity = initial_velocity
current_gear = "1st"
trans_efficiency = 0.9
time = 0
while distance_travelled < total_distance:
    initial_velocity = velocity
    distance_travelled += step
    # print("Distance travelled: ", distance_travelled)
    rpm = calc_rpm_given_speed(1, velocity, car)
    # print("RPM: ", round(rpm, -2))
    torque = rpm_torque.loc[rpm_torque.rpm == round(rpm, -2), "peak_motor_torque"].reset_index(drop=True)[0]
    # print("Torque : ", torque)

    wheel_torque = get_tangent_force_at_wheels(1, torque, car)

    # Calculate the drag force
    drag_force = calculate_drag_force(car, velocity)

    # Calculate the engine force
    engine_force = calculate_engine_force(car, wheel_torque, trans_efficiency)

    # Calculate the friction force
    friction_force = calculate_friction_force(car, velocity)

    # Calculate the new velocity
    velocity = calculate_velocity_new(engine_force,
                                      drag_force, car,
                                      step, velocity)

    time += 1 / (((initial_velocity + velocity) / 2) / step)

    # Print the results
    # print("Drag force: ", drag_force)
    # print("Engine force: ", engine_force)
    # print("Friction force: ", friction_force)
    # print("New velocity: ", velocity)
    # print("Torque: ", wheel_torque)
    # print("")

print("Time: ", time)
