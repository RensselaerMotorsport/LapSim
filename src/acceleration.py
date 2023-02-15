"""Acceleration event calculation."""

from classes.car_simple import Car
from helper_functions_ev import line_segment_time

car = Car("data/rm26.json")

def run_accel(car):
    result = line_segment_time(car, 75, vinitial= 0.001)
    #print(result[1])
    return result[0]

def test_accel(car, LG, UG, n=100):
    car.attrs["gear_ratios"] = LG
    step = (UG - LG) / n
    x = []
    y = []
    for i in range(n):
        x.append(car.attrs["gear_ratios"])
        y.append(run_accel(car))
        car.attrs["gear_ratios"] += step
    import matplotlib.pyplot as plt
    plt.title("Acceleration event times", fontsize=18, y=1.04)
    plt.xlabel("Gear Ratio", fontsize=12)
    plt.ylabel("Time elapsed (s)", fontsize=12)
    plt.plot(x, y, '-g')
    plt.show()

test_accel(car, 5.8, 6.2, n=100)