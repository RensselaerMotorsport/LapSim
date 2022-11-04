car_mass=195
driver_mass=100
frontal_area=1.54
cd=1.41
cl=2.77
trans_efficiency=.9
rho=1.23
wheel_eff_r=.2032
final_drive=6.0085

gear_ratio=np.array([2.75,2,1.667,1.44])

import numpy as np
import math 

RPM=np.array([
4100,
4200,
4300,
4400,
4500,
4600,
4700,
4800,
4900,
5000,
5100,
5200,
5300,
5400,
5500,
5600,
5700,
5800,
5900,
6000,
6100,
6200,
6300,
6400,
6500,
6600,
6700,
6800,
6900,
7000,
7100,
7200,
7300,
7400,
7500,
7600,
7700,
7800,
7900,
8000,
8100,
8200,
8300,
8400,
8500,
8600,
8700,
8800,
8900,
9000,
9100,
9200,
9300,
9400,
9500,
9600,
9700,
9800,
9900,
10000,
10100,
10200,
10300,
10400,
10500,
10600,
10700,
10800,
10900,
11000,
11100,
11200,
11300,
11400,
11500,
11600,
11700,
11800,
11900,
12000,
12100,
12200,
12300,
12400,
12500,
12600,
12700,
12800,
12900,
13000,
13100,
13200,
13300,
13400,
13500,
13600,
13700,
13800,
13900,
14000,
14100,
14200,
14300,
14400,
14500,
14600,
14700,
14800,
14900,
15000,
])

Torque=np.array([
33.187,
33.645,
34.556,
37.118,
39.497,
40.182,
40.662,
41.119,
41.514,
41.918,
42.274,
42.608,
42.836,
42.932,
43.027,
43.05,
43.05,
43.057,
43.081,
43.102,
43.117,
43.111,
42.934,
42.719,
42.423,
42.108,
41.538,
41.047,
40.542,
40.031,
39.571,
39.249,
39.021,
39.066,
39.56,
40.563,
42.139,
43.466,
45.316,
47.019,
48.517,
49.721,
50.43,
51.028,
51.181,
51.1,
50.841,
50.682,
50.51,
50.498,
50.602,
50.958,
51.212,
51.49,
51.823,
52.154,
52.499,
52.706,
52.89,
52.933,
52.914,
52.804,
52.609,
52.332,
51.911,
51.466,
51.039,
50.674,
50.345,
50.095,
49.867,
49.64,
49.44,
49.179,
48.876,
48.603,
48.261,
47.903,
47.51,
47.074,
46.608,
46.131,
45.659,
45.179,
44.621,
43.975,
43.278,
42.577,
41.789,
40.94,
40.156,
39.512,
38.927,
38.481,
38.048,
37.576,
37.192,
36.792,
36.478,
36.142,
35.764,
35.42,
34.989,
34.547,
34.025,
33.414,
32.795,
31.958,
31.175,
30.322,
])

def calc_road_speed(gr,RPM):
    """
    Finds road speed at a given RPM in a given gear as an integer 
    Gears- 0,1,2,3
    """
    return((((RPM/((final_drive*gear_ratio[gr])*trans_efficiency)*6)*3.14)/180)*wheel_eff_r)



def calc_torque(gr,torque):
    """Finds torque at wheels given a gear and torque"""
    return(gear_ratio[gr]*final_drive*trans_efficiency)

def get_engine_force(gr,torque):
    """Finds engine force"""
    return((calc_torque(gr,torque))/wheel_eff_r)

def get_drag_force(velocity):
    """Calculates drag force given a velocity"""
    return((velocity*velocity)*cd*.5*rho*frontal_area)

def solve_v_f(v_i,seg_L,gr):
    """Solves for final velocity of segment given in an initial velocity and segment length"""
    x = get_engine_force()




def calc_corner_radius(coord1, coord2, coord3):
    """
    Calculates radius of corner at any given sector
    Coord1:Starting point of previous sector
    Coord2:Starting point of current sector
    Coord3:Starting point of next sector
    All inputs are in 1D two element numpy arrays
    """
    a = math.sqrt((coord3[1]-coord1[1])**2 + (coord3[2]-coord1[2])**2)
    b = math.sqrt((coord3[1]-coord2[1])**2 + (coord3[2]-coord2[2])**2)
    c = math.sqrt((coord2[1]-coord1[1])**2 + (coord2[2]-coord1[2])**2)
    A = math.acos((b**2+c**2-a**2)/2*b*c)
    return A