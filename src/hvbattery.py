def calc_peak_power(car, Voc): # FUTURE: account for internal resistance thermal sensitivity
    If = car.attrs['max_current']
    series = car.attrs['cells_series']
    parallel = car.attrs['cells_parallel']
    R = car.attrs['cell_resistance']
    Vmin = 2.5

    Im = min(If / parallel, (Voc / series - Vmin) / R)
    return series * parallel * Im * (Voc / series - R * Im)


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
    Vmax = 4.5
    Vmin = 2.5
    return (Vmin + E / Em * (Vmax - Vmin)) * series
