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


def calc_road_speed(gear: int, rpm: int, car, transmission_efficiency: int = 0.9):
    """
    Finds road speed at a given RPM in a given gear as an integer
    Gears- 0,1,2,3
    """
    final_drive = car.attrs["final_drive"]
    tire_radius = car.attrs["tire_radius"]
    gear_ratio = car.attrs["gear_ratio"][gear]

    return ((rpm / (final_drive * gear_ratio * transmission_efficiency) * 6) * 3.14) / 180 * tire_radius


def calc_torque(gear: int, torque: float, car, transmission_efficiency: int = 0.9):
    """Finds torque at wheels given a gear and torque"""
    final_drive = car.attrs["final_drive"]
    gear_ratio = car.attrs["gear_ratio"][gear]

    return torque * gear_ratio * final_drive * transmission_efficiency


def get_engine_force(gear: int, torque: float, car):
    """Finds engine force"""
    tire_radius = car.attrs["tire_radius"]

    return (calc_torque(gear, torque, car)) / tire_radius


def get_drag_force(velocity: float, car):
    """Calculates drag force given a velocity"""
    coeff_drag = car.attrs["Cd"]
    rho = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return velocity**2 * coeff_drag * .5 * rho * frontal_area


# def solve_v_f(v_i, seg_L, gr):
#     """Solves for final velocity of segment given in an initial velocity and segment length"""
#     x = get_engine_force()


def calc_corner_radius(coord1, coord2, coord3):
    """
    Calculates radius of corner at any given sector
    Coord1:Starting point of previous sector
    Coord2:Starting point of current sector
    Coord3:Starting point of next sector
    All inputs are in 1D two element numpy arrays
    """
    a = math.sqrt((coord3[1]-coord1[1])**2 + (coord3[2]-coord1[2])**2)
    b = math.sqrt((coord3[1]-coord2[1])**2 + (coord3[2]-coord2[2])**2)
    c = math.sqrt((coord2[1]-coord1[1])**2 + (coord2[2]-coord1[2])**2)
    return math.acos((b**2+c**2-a**2)/2*b*c)
