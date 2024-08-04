from aerodynamics import calc_down_force
import numpy as np


def calc_max_longitudinal_force(car, v):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']
    g = car.attrs['gravity']
    Fl = calc_down_force(car,v)
    Fz = m * g + Fl

    # u0 = car.attrs['load_sensitivity']
    # return Fz * (mu0 + dmu/dFz * (N0 - Fz))
    ux = car.attrs['CoF']
    return Fz * ux


def calc_max_lateral_force(car, v):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']
    g = car.attrs['gravity']
    Fl = calc_down_force(car,v)
    Fz = m * g + Fl

    # u0 = car.attrs['load_sensitivity']
    # return Fz * (mu0 + dmu/dFz * (N0 - Fz))
    uy = car.attrs['CoF']
    return Fz * uy


def calc_apex_speed(car, ir):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']
    g = car.attrs['gravity']
    p = car.attrs['rho']
    A = car.attrs['A']
    Cl = car.attrs['Cl']
    if isinstance(ir, np.ndarray):
        with np.errstate(divide='ignore', invalid='ignore'):
            r = 1.0 / ir
        r = np.where(np.isfinite(r), r, 1E10)
    elif ir == 0:
        r = 1E10
    else:
        r = 1 / ir
    r = abs(r)

    # u0 = car.attrs['load_sensitivity']
    # return Fz * (mu0 + dmu/dFz * (N0 - Fz))
    uy = car.attrs['CoF']
    weight_grip = m * g * r * uy
    aero_grip = p * A * Cl * r * uy / 2
    # IN FUTURE: reconsider if peak speed considers traction loss to aero drag
    if isinstance(ir, np.ndarray): return np.where(aero_grip >= m, 9999999, (weight_grip / abs(m - aero_grip)) ** 0.5)
    elif aero_grip > m: return 9999999
    else: return (weight_grip / abs(m - aero_grip))**0.5


def calc_rolling_resistance(car, v):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']
    g = car.attrs['gravity']
    Crr = car.attrs['rolling_resistance_coeff']
    Fl = calc_down_force(car, v)
    Fz = m * g + Fl
    return Fz * Crr