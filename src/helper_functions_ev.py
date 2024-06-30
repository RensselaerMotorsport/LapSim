import math
import numpy as np

def motor_torque(car, RPM, voltage=-1, current=-1):
    if voltage == -1: voltage = car.attrs["max_voltage"]
    if current == -1: current = car.attrs["max_current"]

    backemf = car.attrs["induced_voltage"] * RPM
    #voltage -= backemf
    bPower = voltage * current
    maxTorque = car.attrs['max_peak_torque']
    efficiency = car.attrs["tractive_efficiency"] * car.attrs["drivetrain_efficiency"]
    w = RPM * (2*math.pi) / 60
    Kv = car.attrs["constant_kv"]
    Kt = car.attrs["constant_kt"]
    if w == 0: w = 1e-20
    if RPM < voltage * Kv:
        return min(bPower * efficiency / w, maxTorque, current * Kt / (2 ** 0.5))
    else: return 0


def traction_force(car, v, mu):
    g = 9.80665  # m/s^2
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    pr = 1 - car.attrs["proportion_front"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]
    Cd = car.attrs["Cl"]
    h = car.attrs["CG_height"]
    l = car.attrs["wheelbase"]

    return ((rho * A * v**2 * Cl / 2 + m * g * pr) * mu) / (1 - (h * mu) / l)# - rho * A * v**2 * Cd / 2


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


def calc_vmax(r, car):
    mu = car.attrs["CoF"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    Cd = car.attrs["Cd"]
    rho = car.attrs["rho"]
    A = car.attrs["A"]
    Cl = car.attrs["Cl"]

    g = 9.81
    num = (-m*g*Cl*A*(mu**2)*rho*r) - (g*m*mu*(math.sqrt((Cd**2)*(rho**2)*(A**2)*(r**2)+(4*(m**2)))))
    dem = (2*r)*(.25*(rho**2)*(Cl**2)*(A**2)*(mu**2) - .25*(Cd**2)*(rho**2)*(A**2)-((m**2)/(r**2)))

    return (math.sqrt(abs(num/dem)))


def braking_length(car, v0, v1, mu=0, dstep=0.1, returnVal=0):
    if mu == 0: mu = car.attrs["CoF"]

    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    v = v0
    t = 0
    T = []
    d = 0
    V = []
    while v > v1:
        t += dstep/v
        t_seg = dstep/v
        d += dstep
        v -= braking_force(car, v, mu)/m*t_seg
        V.append(v)
        T.append(t_seg)
    if returnVal == 0:
        return t
    elif returnVal == 1:
        return d
    elif returnVal == 2:
        return V
    elif returnVal == 3:
        return T


def forward_int(car, v0, d1, gr=0, mu=0, dstep=0.01):
    if mu == 0: mu = car.attrs["CoF"]
    if gr == 0: gr = car.attrs["final_drive"]
    m = car.attrs["mass_car"] + car.attrs["mass_driver"]
    r = car.attrs["tire_radius"]
    if v0 == 0: v0 = 0.01
    v = [v0]
    d = [0]
    t = [0]
    i = 0
    while d[i] < d1:
        RPM = gr * 60 * v[i] / (2 * math.pi * r)
        a = min((motor_torque(car, RPM) * gr / (r), traction_force(car, v[i], mu))) / m
        v.append((v[i]**2 + 2 * a * dstep)**0.5)
        if a > 0:
            tstep = (- v[i] + (v[i]**2 + 4 * a * dstep)**0.5) / (a)
        else:
            tstep = dstep / v[i]
        t.append(t[i] + tstep)
        d.append(d[i] + dstep)
        i += 1
    return v, d


def straight_line_segment(car, v0, v1, d1, gr=0, mu=0, dstep=0.01, returnV=True):
    if mu == 0: mu = car.attrs('CoF')
    v, d = forward_int(car, v0, d1, gr=gr, mu=mu, dstep=dstep)
    t=0
    for i in range(1,len(v)):
        t += (d[i] - d[i-1]) / v[i]
    if v[len(v)-1] < v1: # If the cornering speed is faster than the max possible speed in straight accel:
        pass
        #print("Max corner speed > max accelerating velocity")
    elif v[len(v)-1] > v1: # If the cornering speed is slower than the max possible speed in straight accel
        dmin = braking_length(car, v0, v1, mu=mu, dstep=dstep, returnVal=1)
        if d1 < dmin: # If the length to brake is greater than the length of the segment
            raise ValueError
        elif d1 == dmin: # The car should brake from start to finish
            return braking_length(car, v0, v1, mu=mu, dstep=dstep, returnVal=2)
        elif d1 > dmin: # The car should accelerate and then brake
            L = len(d)
            vb = v.copy() # Velocities to start braking at
            vb.reverse()
            db = [] # Distances to break from v to v1
            for i in range(len(vb)):
                db.append(braking_length(car, vb[i], v1, mu=mu, dstep=dstep, returnVal=1))
            for i in range(L):
                if abs(d[i] - db[i]) <= 1e-1:
                    v[L-i:L] = braking_length(car, v[L-i], v1, mu=mu, dstep=dstep, returnVal=2)
    if returnV: return v
    else: return t