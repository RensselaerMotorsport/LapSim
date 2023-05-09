"""A module to simulate the acceleration event."""

from classes.car_simple import Car
from helper_functions_ev import forward_int

car = Car("data/rm26.json")

def run_accel(car, GR=0, tmin=4.113, returnPoints=False, peak=False, mu=0):
    """ Calculates the amount of time it takes to run accel. Can return an approximate point value for the event instead of time elapsed.
    Assumptions: Acceleration is 75 m long
    Starting velocity of the car is .001 m/s

    Inputs:
        car: the car object that we are working with
        tmin: best acheieved acceleration time at competition, base value is 4.113 seconds
        returnPoints: if set to True it will return how many points you would earn from accel instead of the time, default is False
    Returns:
        t, the amount of time it takes to complete accel
        or if returnPoints=True, it will return an approximate point value for the event
    """
    if GR == 0: GR = car.attrs["final_drive"]
    t = [0]
    v, d = forward_int(car, 0.001, 75, GR=GR, peak=peak, dstep=0.1, mu=mu) #Call the helper function that runs a straight line segment
    for i in range(1,len(v),1):
        t.append(.1/v[i])
    if returnPoints:
        if t[0] >= 1.5 * tmin: return 4.5 #The time specified is below 150% of the fastest achieved acceleration time, so the point value returned is 4.5 points
        elif t[0] <= tmin: return 100 #The time specified is faster or equal to the fasted achieved acceleration time, maxiumum points have been achieved
        else: return 4.5 + 95.5 * 2 * (1.5 * tmin/t[0] - 1) #The time specfied is slower than the fastest time, but faster than 150% of it, so the stupid equation is used 
    else: return sum(t)


