from classes.car_simple import Car
from helper_functions_ev import straight_line_segment

car = Car("data/rm27.json")

def run_accel(car, gr=0, tmin=3.645, returnPoints=False, mu=0):
    if gr == 0: gr = car.attrs["final_drive"]
    if mu == 0: mu = car.attrs["CoF"]
    t = straight_line_segment(car,1e-5, 100, 75, gr=gr, mu=mu, returnV=False) #Call the helper function that runs a straight line segment
    if returnPoints:
        if t >= 1.5 * tmin: return 4.5 #The time specified is below 150% of the fastest achieved accleration time, so the point value returned is 4.5 points
        elif t <= tmin: return 100 #The time specified is faster or equal to the fasted achieved accleration time, maxiumum points have been achieved
        else: return 4.5 + 95.5 * 2 * (1.5 * tmin/t - 1) #The time specfied is slower than the fastest time, but faster than 150% of it, so the stupid equation is used
    else: return t


def test_accel(car, lg, ug, n=100, returnPoints=False):
    car.attrs["gear_ratios"] = lg  # This is the lowest gear ratio we are going to try
    step = (ug - lg) / n  # This calculates the change in the different gear ratios we are going to try
    x = []
    y = []
    gr = lg
    for i in range(n):  # iterate over all gear ratios
        x.append(gr)
        y.append(run_accel(car, gr=gr, returnPoints=returnPoints))
        gr += step
    import matplotlib.pyplot as plt  # Create the plot of gear ratio versus time
    plt.xlim(lg, ug)
    plt.grid()
    if returnPoints: plt.title("Acceleration event points", fontsize=18, y=1.04)
    else: plt.title("Acceleration event times", fontsize=18, y=1.04)
    plt.xlabel("Gear Ratio", fontsize=12)
    if returnPoints: plt.ylabel("Points scored", fontsize=12)
    else: plt.ylabel("Time elapsed (s)", fontsize=12)
    plt.plot(x, y, '-g')
    plt.show()
