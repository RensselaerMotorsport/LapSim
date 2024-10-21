from classes.car_simple import Car
from simulator import Competition
import numpy as np

car = Car("data/rm28.json")
MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')



def sweep_parallel_count():
    x = np.array([])
    y = np.array([])
    for i in range(6,11):
        car.attrs["mass_battery"] += 0.057 * 95
        car.attrs['cells_parallel'] = i
        xi, yi = MIS_2019.sweep_var(car, 'power_limit', 10, 10000, 80000, count=2)
        x = np.append(x, xi)
        y = np.append(y, yi)
    print(x)
    print(y)
