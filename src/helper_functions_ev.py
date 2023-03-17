"""A module to calculate intermediate steps in the lapsim for an ev car"""

import math

def calc_vmax(r, car):
    """
    Calculates the maximum velocity for a corner given it's radius. 
    """
    mew = car.attrs["CoF"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    Cd = car.attrs["Cd"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]

    g = 9.8 


    num = (-m*g*Cl*A*(mew**2)*rho*r) - (g*m*mew*(math.sqrt((Cd**2)*(rho**2)*(A**2)*(r**2)+(4*(m**2)))))
    dem = (2*r)*(.25*(rho**2)*(Cl**2)*(A**2)*(mew**2) - .25*(Cd**2)*(rho**2)*(A**2)-((m**2)/(r**2)))

    return (math.sqrt(abs(num/dem)))
    #There are 4 possible solutions to this problem. Two have been selected (through abs) as possible real solutions as the others are negative. 
    #The other two solutions differ by the minus or plus sign in the numerator between both large terms.
    #The negative sign was chosen as the only real solution because this yields real results when changing Cl on skidpad. 
    #It is possible that this solution does not always yield a real result and the other solutions are real but this will be something we come back to. 
    
    #This model includes 

def calc_max_entry_v_for_brake(car, Vexit, r, d):
    """
    A function to calculate the max entry speed for a given sement in 
    which the car could have braked to a given veloicty at the end of the segment

    Car - Car Object
    Vexit - Exit Velocity of previous segment
    r = radius of segment
    d = segment length
    """
    g = 9.8 #m/s^2
    mew = car.attrs["CoF"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    Cd = car.attrs["Cd"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]

    friction_force = ((mew**2)*(m*g + .5*rho*Cl*A*Vexit**2)**2)
    centripetal_force = ((m**2)*(Vexit**4))/(r**2)

    Drag = Cd*.5*rho*A*Vexit**2
    if r < 1e-6:
        Fb = math.sqrt((mew**2)*(m*g + .5*rho*Cl*A*Vexit**2)**2)
    else:
        if friction_force < centripetal_force:
            raise ValueError("Friction force is smaller than centripetal force, tires are slipping!")
        Fb = math.sqrt(friction_force-centripetal_force)
    Fs = Drag + Fb

    u = math.sqrt(Vexit**2+(2*d*Fs)/m)

    return u 



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

def line_segment_time(car, distance, vinitial=0.001, timestep=.001):
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
    while d<distance:
        RPM = 60 * v / (2 * math.pi * car.attrs["tire_radius"]) * car.attrs["gear_ratios"]
        acceleration = motor_torque(car, RPM, peak=True) * car.attrs["gear_ratios"] / (car.attrs["tire_radius"] * (car.attrs["mass_car"] + car.attrs["mass_driver"]))
        time+=timestep
        d+=v*timestep
        v+=acceleration*timestep
    return time, v

def motor_torque(car, RPM, peak=False, voltage=0, current=0):
    """do docstring here at some point. Torque = Current * Voltage / RPM.

    :param car:
    :param RPM: motor RPM
    :param peak:
    :param voltage:
    :param current:
    :return:
    """
    if voltage == 0 : voltage = car.attrs["max_voltage"]
    if current == 0 : current = car.attrs["max_current"]
    maxCTorque = 130 # Emrax 228 HV
    maxPTorque = 230 # Emrax 228 HV
    if RPM < voltage / 0.07348: # Only works for Emrax 228
        if peak:
            return min(60 / (2*math.pi) * current * voltage / RPM, maxPTorque) # Converts RPM -> angular velocity
        else:
            return min(60 / (2*math.pi) * current * voltage / RPM, maxCTorque)
    else: return 0

