"""A module to calculate the velocities and time for a Skid Pad"""

from classes.car_simple import Car
from helper_functions_ev import calc_vmax
import numpy as np

#car = Car("data/rm26.json")


### Below is a troubleshooting script ###

# OR = 18.25   #Outer radius
# IR = 15.25   #Inner radius
# Mid = 16.75  #Middle radius

# V_O = calc_vmax(OR, car) #Calculate maximum possible velocity traveling the outer corner radius
# V_I = calc_vmax(IR, car) #Calculate the maxiumium possible velocity traveling the inner corner radius
# V_M = calc_vmax(Mid,car) #Calculate the maxiumum possible velocity while traveling the middle corner radius

# circum_O = 2*3.14*OR #Circumference of the circle with the outer radius
# circum_I = 2*3.14*IR #Circumference of the circle with the inner radius
# circum_M = 2*3.14*Mid   #Circumference of the circle with a middle radius

# # print("Velocity Outer =", V_O)
# # print("Velocity Inner =", V_I)
# # print("Velocity Middle =", V_M)


# t_O = circum_O/V_O #Time taken to traverse the outer radius
# t_I = circum_I/V_I #Time taken to traverse the inner radius
# t_M = circum_M/V_M #Time taken to traverse the middle radius

# # print("Time Outer =",t_O)
# # print("Time_Inner =",t_I)
# # print("Time_Middle =",t_M)

# #This model will likely predict a slower skidpad time than in real life because the tire model is basically non existent.



def skidpad(r, car):
    """
    A function that takes the radius of the skidpad course and a car object to calculate the amount of time it will take to complete a skipad run.

    Inputs: r, the radius of the skipad circle
    car, the car object with the json values

    Output: t, the amount of time skipad takes
    """
    v = calc_vmax(r,car)
    circum = 2*3.14*r
    t = circum/v

    return t, v


def test_skidpad(car, step=1000, returnPoints=False, printStats=False):
    """A function to calculate the time elapsed or points earned at the skidpad dynamic event.

    :param car: Car dictionary
    :param step: Testing resolution
    :param returnPoints: If True: returns points earned, if False: returns time elapsed
    :return: Returns a value of time or points earned
    """
    radii = np.linspace(7.625, 10.625, step)
    times = np.zeros(step)
    for i in range(radii.size):
        times[i] = skidpad(radii[i], car)[0]
    t = times.min()
    if printStats:
        for k, j in np.ndenumerate(times):
            if j == t:
                indx = k
        r = radii[indx]
        print(r)
        v = calc_vmax(radii[indx], car)
        print(v)
        print(v ** 2 / r / 9.81)
        print(times[indx])
    if returnPoints:
        if t <= 5.046:
            y = 75
        elif t > 1.25 * 5.046:
            y = 3.5
        else:
            p = 3.5 + 71.5 * 16/9 * ((1.25 * 5.046 / t)**2 - 1)
            y = p
    else:
        y = t
    return y

#print(test_skidpad(car, returnPoints=False))
#print(skidpad(IR,car))

