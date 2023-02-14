"""A module to calculate intermediate steps in the lapsim for an ev car"""

import math

def calc_vmax(r, car):
    """
    Calculates the maximum velocity for a corner. 
    """
    mew = car.attrs["CoF"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    Cd = car.attrs["Cd"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]

    g = 9.8 


    num = 2*r*((-g*m*rho*Cl*A*r*mew**2) + (g*m*mew*(math.sqrt((Cd**2)*(rho**2)*(A**2)*(r**2)+(4*m**2)))))
    dem = (r**2)*((rho**2)*(Cl**2)*(A**2)*(mew**2) - (Cd**2)*(rho**2)*(A**2)) - 4*(m**2)
    return math.sqrt(num/dem)


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

    
def get_drag_force(velocity: float, car):
    """Calculates drag force given a velocity"""
    coeff_drag = car.attrs["Cd"]
    rho = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return velocity**2 * coeff_drag * .5 * rho * frontal_area

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



def straightlinesegmenttime(car, distance, vinitial=0.001, torque=120, timestep=.001):
    """
    Calculates the amount of time it takes to travel a straight line distance.
    
    Inputs:
    car- the car object with attributes
    vinitial- the initial velocity into the segment
    distance- how long the segment is
    
    Outputs:
    t- the amount of time it takes to complete the segment."""
    d=0
    v=vinitial
    time=0
    acceleration=torque*car.attrs["gear_ratios"]/(car.attrs["tire_radius"]*(car.attrs["mass_car"]+car.attrs["mass_driver"]))
    while d<distance:
        time+=timestep
        d+=v*timestep
        v+=acceleration*timestep
    return time, distance

