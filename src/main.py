from classes.car_simple import Car
from simulator import Competition
import numpy as np


car = Car("data/rm28.json")

MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')

#x, y = MIS_2019.sweep_var(car, 'power_limit', 10, 10000, 80000, count=5)
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

# plot_single_yaxis(x, y, 'Cells in parallel','Laptime (s)',['6P','7P','8P','9P','10P'],['#0149fe','#00637a','#005a64','#00583d','#2e4d1a'],['-','-','-','-','-','-','-','-','-','-'])

#MIS_2019.draw_plots(car)
#MIS_2019.plot_power_limits(10000,60000,count=40)
