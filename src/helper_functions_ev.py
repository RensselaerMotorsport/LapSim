"""A module to calculate intermediate steps in the lapsim for an ev car"""

import math

def calc_vmax(r, car):
    """
    Calculates the maximum velocity for a corner given it's radius.

    Inputs:
    r, the radius of the corner
    car, the car object we are considering

    Returns:
    The maximium velocity the car can go around the corner 
    """
    mew = car.attrs["CoF"] #Coefficent of friction of the car object
    m = car.attrs["mass_car"] + car.attrs["mass_driver"] #Total mass of the car object and driver
    Cd = car.attrs["Cd"] #Coefficent of drag for the car object
    rho = car.attrs["rho"] #Density of air from the car object
    A = car.attrs["A"] #Frontal wing area of the car object
    Cl = car.attrs["Cl"] #coefficent of lift for the car object

    g = 9.8 #Assign the acclertion due to gravity


    num = (-m*g*Cl*A*(mu**2)*rho*r) - (g*m*mu*(math.sqrt((Cd**2)*(rho**2)*(A**2)*(r**2)+(4*(m**2)))))
    dem = (2*r)*(.25*(rho**2)*(Cl**2)*(A**2)*(mu**2) - .25*(Cd**2)*(rho**2)*(A**2)-((m**2)/(r**2)))

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
    mu = car.attrs["CoF"] #Coefficent of Friction of the car object
    m = car.attrs["mass_car"] + car.attrs["mass_driver"] #Total mass of the car object and driver
    Cd = car.attrs["Cd"]#Coefficent of drag for the car object
    rho = car.attrs["rho"]#Density of air for the car object
    A = car.attrs["A"] #Frontal wing area of the car object
    Cl = car.attrs["Cl"] #Coefficent of lift for the car object

    Drag = Cd*.5*rho*A*Vexit**2 #Calculate the drag of th car
    if r < 1e-6: #for really small radi
        Fb = math.sqrt((mu**2)*(m*g + .5*rho*Cl*A*Vexit**2)**2) #Calculate the breaking force
    else:
        Fb = math.sqrt(((mu**2)*(m*g + .5*rho*Cl*A*Vexit**2)**2) - ((m**2)*(Vexit**4))/(r**2)) #Calculate the braking force
    Fs = Drag + Fb #sum up the overal force

    u = math.sqrt(Vexit**2+(2*d*Fs)/m) #Calculate the maximium entry velocity

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
    car_mass = car.attrs["mass_car"] #mass of the car in the car object
    driver_mass = car.attrs["mass_driver"] #mass of the driver in the car object

    return math.sqrt((initial_velocity**2) + 2 * step * ((engine_force - drag_force) / (car_mass + driver_mass))) #calculate velocity at the end of a time step

    
def get_drag_force(velocity: float, car):
    """Calculates drag force given a velocity
    
    Given: Velocity as a float, the velocity you are calculating the drag force for
    car, the car object you are considering

    Returns: the drag force at that velocity
    """
    coeff_drag = car.attrs["Cd"] #The coefficent of drag in the car object
    rho = car.attrs["rho"] #The density of air in the car object
    frontal_area = car.attrs["A"] #The frontal area of the car in the car object

    return velocity**2 * coeff_drag * .5 * rho * frontal_area #Formula for drag force

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

def line_segment_time(car, distance, GR=0, vinitial=0.001, timestep=.001, peak=False, mu=0):
    """
    Calculates the amount of time it takes to travel a straight line distance.

    Inputs:
    car- the car object with attributes
    vinitial- the initial velocity into the segment
    distance- how long the segment is

    Outputs:
    t- the amount of time it takes to complete the segment."""
    d=0 #Set initial distance object
    v=vinitial #initial velocity
    time=0 #Set time variable
    if GR == 0: GR = car.attrs["final_drive"]
    if mu == 0: mu = car.attrs["CoF"]
    r = car.attrs["tire_radius"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    while d<distance: 
        RPM = 60 * v / (2 * math.pi * r) * GR
        acceleration = (min((motor_torque(car, RPM, peak=peak) * GR / (r), traction_force(car, v, mu))) - rho * A * v**2 / 2)/ m
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
    backemf = car.attrs["induced_voltage"] * RPM
    voltage -= backemf # Accounts for back emf at higher RPM
    bPower = voltage * current
    maxCTorque = 130 # Emrax 228 HV
    maxPTorque = 230 # Emrax 228 HV
    efficiency = car.attrs["tractive_efficiency"] * car.attrs["drivetrain_efficiency"]
    w = RPM * (2*math.pi) / 60
    Kv = car.attrs["constant_kv"]
    if RPM < (voltage + backemf) * Kv:
        if peak:
            return min(bPower * efficiency / w, maxPTorque) # Accounts for drivetrain & tractive efficiencies
        else:
            return min(bPower * efficiency / w, maxCTorque)
    else: return 0

def traction_force(car, v, mu):
    g = 9.80665  # m/s^2
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]
    Cd = car.attrs["Cl"]
    h = car.attrs["CG_height"]
    l = car.attrs["wheelbase"]
    return ((rho * A * v**2 * Cl / 2 + m * g) / 2 * mu) / (1 - (h * mu) / l)# - rho * A * v**2 * Cd / 2

def braking_force(car, v, mu):
    g = 9.80665  # m/s^2
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]
    Cd = car.attrs["Cd"]
    h = car.attrs["CG_height"]
    l = car.attrs["wheelbase"]
    return ((rho * A * v**2 * Cl / 2 + m * g) / 2 * mu) / (1 + (h * mu) / l) + rho * A * v**2 * Cd / 2
