"""A module to calculate intermediate steps in the lapsim for an ev car"""

import math


def calculate_velocity_new(engine_force, drag_force, car, step=1, initial_velocity=0.001):
    """
    A function for calculating the velocity at the end of a time step.
    
    Given: engine_force, the engine force at the begining of the time step calculated from the calculate_engine_force function
    drag_force, the drag force at the begining of the time step calculated from the calculate_drag_force function
    car, the car object we are testing
    step, the time step we are at, default is 1
    initial velocity, the initial velocity at the time step, default is .001
    
    Returns: the velocity at the end of the time step
    """
    car_mass = car.attrs["mass_car"]
    driver_mass = car.attrs["mass_driver"]

    return math.sqrt((initial_velocity**2) + 2 * step * ((engine_force - drag_force) / (car_mass + driver_mass)))


def calculate_drag_force(car, initial_velocity=0.001):
    """
    A function for calculating the drag force of a provided car at a provided velocity.
    
    Given: car, the car object we are testing
    initial_velocity, the velocity at the begining of the time step we are running, default is .001
    
    Returns: the drag froce of the car at the provided velocity
    """
    coeff_drag = car.attrs["Cd"]
    air_density = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return coeff_drag * 0.5 * air_density * (initial_velocity ** 2) * frontal_area


def calculate_friction_force(car, initial_velocity=0):
    """
    A function for calculating the friction force of a car at an initial velocity.
    
    Given: car, the car object we are testing
    initial_velocity, the initial velocoty of the car at a time step, default is 0
    
    Returns: the friction force at the provided conditions.
    """
    coeff_friction = car.attrs["CoF"]
    car_mass = car.attrs["mass_car"]
    driver_mass = car.attrs["mass_driver"]
    coeff_lift = car.attrs["Cl"]
    air_density = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return coeff_friction * ((car_mass + driver_mass) * 9.81) + (coeff_lift * 0.5 * air_density * (initial_velocity**2) * frontal_area)

    
def get_drag_force(velocity: float, car):
    """Calculates drag force given a velocity"""
    coeff_drag = car.attrs["Cd"]
    rho = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return velocity**2 * coeff_drag * .5 * rho * frontal_area


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


def calc_lat_accel(car, v, icr):
    """
    Calculates lateral acceleration

    Imputs:
    car - object car
    v - velocity in m/s
    icr - inverse corner radius in rad

    Output:
    Lateral acceleration in m/s**2
    """
    return ((car.attrs["mass_car"])*(v**2))/icr

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
