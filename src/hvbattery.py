def calc_peak_power(car, Voc):
    # FUTURE: account for internal resistance thermal sensitivity
    # FUTURE: account for internal resistance sensitivity to current draw
    Ifuse = car.attrs['fuse_current']
    Ilimit = car.attrs["current_limit"]
    series = car.attrs['cells_series']
    parallel = car.attrs['cells_parallel']
    R = car.attrs['cell_resistance']
    vmin = 2.5
    voc = Voc / series

    Imin = min(Ifuse / parallel, Ilimit / parallel)
    pmax = R * ((voc / (2*R))**2 - (voc / (2*R) - Imin)**2)
    ppk = vmin * (voc - vmin) / R
    return series * parallel * min(pmax, ppk)


def calc_heat_gen(car, Voc, P):
    R = car.attrs['cell_resistance']
    series = car.attrs['cells_series']
    parallel = car.attrs['cells_parallel']
    Voc /= series
    P /= series * parallel

    I = Voc / (2 * R) - (Voc**2 / (4 * R**2) - P / R)**0.5
    return (I**2 * R) * series * parallel


def calc_Voc(car, E):
    series = car.attrs['cells_series']
    parallel = car.attrs['cells_parallel']
    capacity = car.attrs['cell_capacity']
    Em = series * parallel * capacity * 3600
    Vmax = 4.2
    Vmin = 2.5
    return (Vmin + E / Em * (Vmax - Vmin)) * series
