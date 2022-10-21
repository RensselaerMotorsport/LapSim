import math


def calculate_velocity_new(engine_force, drag_force, car_mass, driver_mass, step = 1, initial_velocity = 0.001):
    return math.sqrt((initial_velocity**2) + 2 * step * ((engine_force - drag_force) / (car_mass + driver_mass)))


def calculate_drag_force(coeff_drag, air_density, frontal_area, initial_velocity = 0.001):
    return coeff_drag * 0.5 * air_density * (initial_velocity ** 2) * frontal_area


def calculate_engine_force(wheel_torque, trans_efficiency, tire_radius):
    return (wheel_torque * trans_efficiency) / tire_radius


def calculate_friction_force(coeff_friction, car_mass, driver_mass, coeff_lift, air_density, frontal_area, initial_velocity = 0):
    return coeff_friction * ((car_mass + driver_mass) * 9.81) + (coeff_lift * 0.5 * air_density * (initial_velocity**2) * frontal_area)


def find_torque_given_velocity(velocity: float, wheel_torque, rpm_v_road_speed, rpm_torque, gear: str = "1st"):
    rpm = 0
    for _, row in rpm_v_road_speed.iterrows():
        if row[gear] < velocity:
            rpm = row["RPM"]
        else:
            break
    print(rpm)
    print(rpm_torque.loc[rpm_torque.rpm == rpm, 'torque'])
    engine_torque = rpm_torque.loc[rpm_torque.rpm == rpm, 'torque'].reset_index(drop=True)[0]

    torque = 0
    for _, row in wheel_torque.iterrows():
        if row["T"] < engine_torque:
            torque = row[gear]
        else:
            break

    return torque
