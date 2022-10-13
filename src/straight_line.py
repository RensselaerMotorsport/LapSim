from helper_functions import calculate_drag_force,\
    calculate_engine_force, \
    calculate_velocity_new, \
    calculate_friction_force, \
    find_torque_given_velocity

from classes.car_simple import Car

import pandas as pd

gear_torque = pd.read_csv("./data/torque_for_each_gear.csv")
rpm_v_road_speed = pd.read_csv("./data/rpm_vs_road_speed.csv")
rpm_torque = pd.read_csv("./data/rpm_torque.csv")

step = 0.1  # meters
initial_velocity = 0.01  # meters per second

car = Car("data/rm25.json")

distance_travelled = 0
total_distance = 75  # meters

velocity = initial_velocity
current_gear = "1st"
trans_efficiency = 0.9

while distance_travelled < total_distance:
    distance_travelled += step
    print("Distance travelled: ", distance_travelled)

    wheel_torque = find_torque_given_velocity(velocity,
                                              gear_torque,
                                              rpm_v_road_speed,
                                              rpm_torque, current_gear)

    # Calculate the drag force
    drag_force = calculate_drag_force(car.attrs["Cd"],
                                      car.attrs["rho"],
                                      car.attrs["A"], velocity)

    # Calculate the engine force
    engine_force = calculate_engine_force(wheel_torque,
                                          trans_efficiency,
                                          car.attrs["tire_radius"])

    # Calculate the friction force
    friction_force = calculate_friction_force(car.attrs['CoF'],
                                              car.attrs['mass_car'],
                                              car.attrs['mass_driver'],
                                              car.attrs['Cl'],
                                              car.attrs['rho'],
                                              car.attrs['A'], velocity)

    # Calculate the new velocity
    velocity = calculate_velocity_new(engine_force,
                                      drag_force,
                                      car.attrs['mass_car'],
                                      car.attrs['mass_driver'],
                                      step, velocity)

    # Print the results
    print("Drag force: ", drag_force)
    print("Engine force: ", engine_force)
    print("Friction force: ", friction_force)
    print("New velocity: ", velocity)
    print("Torque: ", wheel_torque)
    print("")
