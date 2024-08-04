def calc_down_force(car, v):
    p = car.attrs['rho']
    A = car.attrs['A']
    Cl = car.attrs['Cl']
    return p * A * Cl * v**2 / 2


def calc_drag_force(car, v):
    p = car.attrs['rho']
    A = car.attrs['A']
    Cd = car.attrs['Cd']
    return p * A * Cd * v**2 / 2
