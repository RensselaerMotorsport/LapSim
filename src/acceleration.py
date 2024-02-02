"""A module to simulate the acceleration event."""

from classes.car_simple import Car
from helper_functions_ev import straight_line_segment

car = Car("data/rm27.json")

def run_accel(car, GR=0, tmin=3.645, returnPoints=False, peak=False, mu=0):
    """ Calculates the amount of time it takes to run accel. Can return an approximate point value for the event instead of time elapsed.
    Assumptions: Acceleration is 75 m long
    Starting velocity of the car is .001 m/s

    Inputs:
        car: the car object that we are working with
        tmin: best achieved acceleration time at competition, base value is 3.645 seconds
        returnPoints: if set to True it will return how many points you would earn from accel instead of the time, default is False
    Returns:
        t, the amount of time it takes to complete accel
        or if returnPoints=True, it will return an approximate point value for the event
    """
    if GR == 0: GR = car.attrs["final_drive"]
    if mu == 0: mu = car.attrs["CoF"]
    t = straight_line_segment(car,0.00001, 100, 75, GR=GR, peak=peak, mu=mu, returnV=False) #Call the helper function that runs a straight line segment
    if returnPoints:
        if t >= 1.5 * tmin: return 4.5 #The time specified is below 150% of the fastest achieved accleration time, so the point value returned is 4.5 points
        elif t <= tmin: return 100 #The time specified is faster or equal to the fasted achieved accleration time, maxiumum points have been achieved
        else: return 4.5 + 95.5 * 2 * (1.5 * tmin/t - 1) #The time specfied is slower than the fastest time, but faster than 150% of it, so the stupid equation is used
    else: return t


def test_accel(car, LG, UG, n=100, returnPoints=False, peak=False):
    # THIS FUNCTION IS BROKEN RIGHT NOW
    """A function for testing the response of our run_accel function.

    Inputs: car, the car object we are working with
    LG, the car's lower bound gear ratio
    UG, the car's upper bound gear ratio
    n, this equals the number of gear ratios that we want to test, default is 100
    returnPoints, this determines if the function returns point values or time values for accleration, default is False which returns time values

    Returns: A plot of gear ratios tried to point values achieved if returnPoints=False, or to time is returnPoints=True"""
    car.attrs["gear_ratios"] = LG  # This is the lowest gear ratio we are going to try
    step = (UG - LG) / n  # This calculates the change in the different gear ratios we are going to try
    x = []
    y = []
    GR = LG
    for i in range(n):  # iterate over all gear ratios
        x.append(GR)
        y.append(run_accel(car, GR=GR, returnPoints=returnPoints, peak=peak))
        GR += step
    import matplotlib.pyplot as plt  # Create the plot of gear ratio versus time
    plt.xlim(LG,UG)
    plt.grid()
    if returnPoints: plt.title("Acceleration event points", fontsize=18, y=1.04)
    else: plt.title("Acceleration event times", fontsize=18, y=1.04)
    plt.xlabel("Gear Ratio", fontsize=12)
    if returnPoints: plt.ylabel("Points scored", fontsize=12)
    else: plt.ylabel("Time elapsed (s)", fontsize=12)
    plt.plot(x, y, '-g')
    plt.show()
