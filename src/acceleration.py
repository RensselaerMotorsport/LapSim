"""Acceleration event calculation."""

from classes.car_simple import Car
from helper_functions_ev import line_segment_time

car = Car("data/rm26.json")

def run_accel(car, tmin=4.113, returnPoints=False):
    """ Calculates time to travel 75 m in a straight line. Can return points instead of time elapsed.

    car: car
    tmin: Best achieved accel time at comp
    returnPoints: Whether or not to return results as point values or time values
    return:
    """
    t = line_segment_time(car, 75, vinitial= 0.001)
    if returnPoints:
        if t[0] >= 1.5 * tmin: return 4.5
        elif t[0] <= tmin: return 100
        else: return 4.5 + 95.5 * 2 * (1.5 * tmin/t[0] - 1)
    else: return t[0]

def test_accel(car, LG, UG, n=100, returnPoints=False):
    car.attrs["gear_ratios"] = LG
    step = (UG - LG) / n
    x = []
    y = []
    for i in range(n):
        x.append(car.attrs["gear_ratios"])
        y.append(run_accel(car, returnPoints=returnPoints))
        car.attrs["gear_ratios"] += step
    import matplotlib.pyplot as plt
    plt.title("Acceleration event times", fontsize=18, y=1.04)
    plt.xlabel("Gear Ratio", fontsize=12)
    plt.ylabel("Time elapsed (s)", fontsize=12)
    plt.plot(x, y, '-g')
    plt.show()

test_accel(car, 0.1, 10, returnPoints=True)
