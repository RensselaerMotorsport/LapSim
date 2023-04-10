"""A module to simulate Oval"""

from helper_functions_ev import calc_vmax
from helper_functions_ev import forward_int
from helper_functions_ev import braking_length
from helper_functions_ev import straight_line_segment
from classes.car_simple import Car
from random import random
import numpy as np
import math
car = Car("data/rm26.json")



#Set Parameters for track
straight_d = 77  #Range 61-77
corner_r = 15    #Range 15-25
n = (straight_d*2)+2  #number of segments

#Track is a two element array that stores the distance of a segment in the first column and its radius in the second
track = np.zeros((n+1,2))

#Create Track Using Parameters
for i in range(n):
    track[i,0] = straight_d/straight_d
#print(track)

#Add Corners for the Oval 
track[straight_d+1,1] = corner_r
track[straight_d+1,0] = 2*math.pi*corner_r
track[(straight_d*2)+1,1] = corner_r
track[(straight_d*2)+1,0] = 2*math.pi*corner_r
track[n,0] = 0
track[n,1] = 0



def runtrack(Car, track):
    """
    A function to run the oval track given the car object, straight distance, and corner radius and output a time. 
    
    Parameters:
    Car - car object
    track - 2-D array of distance and radius

    Return - Track Time
    """
    #Initialize time and velocity arrays, time will be output and velocity can be conditional output (In future)
    time = np.zeros(track.size)
    velocity = np.zeros(track.size)
    velocity[0] = .0001
    
    for i in range(track.size):
        iter = i+1
        if iter == n:
            break

        #print("Iter =",iter)
        #print("Velocity =",velocity[i])
        #print("Radius =",track[i,1])
        #print("Distance=",track[i,0])

        if track[i,1] == 0:
            time[i+1],velocity[i+1] = forward_int(Car, velocity[i],track[i,0], dstep=0.0001)#velocity[i+1] is the exit velocity
            print(velocity)
        else:
            vmax = calc_vmax(corner_r,Car)
            #print("Vmax=", vmax)
            if velocity[i] < vmax or velocity[i] == vmax:
                time[i+1] = (math.pi*corner_r)/velocity[i]
                velocity[i+1] = velocity[i]
            elif velocity > vmax:
                for j in range(1,77):
                    d = braking_length(Car,velocity[-j],vmax,returnVal=1)
                    if d - 77-j < 1:
                        velocity[j:] = braking_length(Car,velocity(-j),vmax,returnVal=2)
                        time[j:] = braking_length(Car,velocity(-j),vmax,returnVal=3)
                time[i+1] = (math.pi*corner_r)/vmax
                velocity[i+1] = vmax



    return ("Lap Time is", np.sum(time, axis=None))

#print(runtrack(car, track))


#plt.plot(forward_int(Car, 0,27,returnVal=0),forward_int(Car, 0,27,returnVal=1))
#plt.show

def run_oval(car, x, r, GR=0, mu=0, dstep=0.01, peak=False):
    d = [0] # Car distance travelled
    v = [0] # Car speed
    for i in range(len(x)):
        if r[i] == 0: # Straight segment
            v1 = straight_line_segment(car, v[len(v) - 1], calc_vmax(1 / r[i+1], car), x[i], GR=GR, mu=mu, dstep=dstep, peak=peak)
            for j in range(1, len(v1), 1):
                v.append(v1[j])
                d.append(dstep + d[len(d) - 1])
        else:
            v1 = min(calc_vmax(1 / r[i], car), v[len(v) - 1])
            for j in np.arange(0, x[i], dstep):
                v.append(v1)
                d.append(dstep + d[len(d) - 1])
    return d, v

def s_pin():
    return 10 + random() * 50

def s_wide():
    return 10 + random() * 35

def r_const():
    return 1 / (23/2 + random() * 11)

def r_pin():
    return 1 / (4.5 + random() * 4.5)

def construct_track(dist):
    """
    The Autocross course will be designed with the following specifications. Average speeds
    should be 40 km/hr to 48 km/hr
        a. Straights: No longer than 60 m with hairpins at both ends
        b. Straights: No longer than 45 m with wide turns on the ends
        c. Constant Turns: 23 m to 45 m diameter
        d. Hairpin Turns: 9 m minimum outside diameter (of the turn)
        e. Slaloms: Cones in a straight line with 7.62 m to 12.19 m spacing
        f. Miscellaneous: Chicanes, multiple turns, decreasing radius turns, etc.
        g. Minimum track width: 3.5 m
        h. Length of each run should be approximately 0.80 km
    """
    x = []
    r = []
    i = 0
    while sum(x) < dist or i % 2 != 0:
        if i % 2 != 0:
            # Assume turns are between 100 & 170 degree turns
            r.append(r_const())
            x.append(2 * math.pi / r[i] * (100 + 70 * random()) / 360)
        else:
            x.append(s_wide())
            r.append(0)
        i += 1
    return x, r

x, r = construct_track(800)


from time import perf_counter
def plot_graph(GR):
    t0 = perf_counter()
    d, v = run_oval(car, x, r, GR=GR)

    t = 0
    for i in range(1, len(d), 1):
        t += (d[i] - d[i - 1]) / v[i]

    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings("ignore")

    for i in range(len(v)):
        v[i] *= 2.237

    plt.figure(figsize=(9,6))
    plt.grid()
    plt.xlim(0, d[len(d) - 1] * 1.01)
    plt.ylim(0, max(v) * 1.05)

    plt.plot(d, v)
    plt.title(str(round(t,3)) + " seconds; " + str(round(d[len(d) - 1] / t * 2.237, 1)) + " mph average")
    plt.suptitle(str(round(GR,2)) + " Gear ratio")
    plt.xlabel("Distance (m)")
    plt.ylabel("Velocity (mph)")
    plt.show()
    t1 = perf_counter()
    return t1 - t0

print(round(plot_graph(33/12), 5))
print(round(plot_graph(38/12), 5))
print(round(plot_graph(42/12), 5))