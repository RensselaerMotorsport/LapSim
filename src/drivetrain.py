import math
pi = math.pi


def calc_wheel_force(car, v, pbm):
    TM = car.attrs['peak_torque']
    HVeff = car.attrs['tractive_efficiency']
    DTeff = car.attrs['drivetrain_efficiency']
    GR = car.attrs['gear_ratio']
    rT = car.attrs['tire_radius']
    kV = car.attrs['constant_kv']
    V = car.attrs['cells_series'] * 4.5
    # ^ IN FUTURE CALL FROM BATTERY MODEL
    if v == 0: v = 1E-10
    MRPM = v * GR * 60 / (2 * pi * rT)
    if MRPM >= kV * V: return 0

    motor_lim = TM
    rules_lim = 80000 * HVeff * 30 / (MRPM * pi)
    battery_lim = pbm * HVeff * 30 / (MRPM * pi)
    power_lim = car.attrs['power_limit'] * HVeff * 30 / (MRPM * pi)
    return min(motor_lim, rules_lim, battery_lim, power_lim) * DTeff * GR / rT
