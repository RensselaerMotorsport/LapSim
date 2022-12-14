"""A module to model the weight transfer of a four tire vehicle"""

########Limitations########
#Neglects dampering effects of suspension system
#neglects any tire slip and thus tire deformation
#neglects the effect of heat on tires
#neglects difference in areas between front and rear (uses one param - frontal area) important for aero analysis
#neglects changes in aero loads in yaw



import numpy as np

g = 9.8 #m/s^2
mass_car = 195 #kg
mass_driver = 100 #kg
W = g*(mass_car+mass_driver) #N
Cf = 1.6 #coef of friction

########Check Vehicle Dynamics chapter 18 for explination on these parameters########

h = .323879 #COG height in m
L = 1.525 #wheelbase in m

y_ = .60137 #m
Y_ = .00737 #m

b_ = .92564 #m
a_ = .59936 #m

Tf = 1.228 #track length front in m
Tr = 1.188 #track length rear in m

Steady_weight = np.array([353.63, 298.12, 591.61, 569.37]) #array of steady state tire loads with entry [0] equal to tire number 1

offset_ratio_F = (Y_*2)/(Tf/2)
offset_ratio_R = (Y_*2)/(Tr/2)

### Coef for longitudinal weight transfer###
Cx1 = 1/2*(1-offset_ratio_F)
Cx2 = 1/2*(1+offset_ratio_F)
Cx3 = 1/2*(1-offset_ratio_R)
Cx4 = 1/2*(1+offset_ratio_R)

def calc_long_weight_transfer(ax, t_no):
    """
    Calculates weight transfer due to longitudinal acceleration
    
    Inputs: 
    ax - Longitudinal Acceleration
    t_no - tire number

    Outputs:
    weight_transfer - weight transfer of tire
    """
    
    if t_no == 1:
        return -Cx1*W*(h/L)*(ax/g)
    elif t_no == 2:
        return -Cx2*W*(h/L)*(ax/g)
    elif t_no == 3 :
        return Cx3*W*(h/L)*(ax/g) 
    elif t_no == 4:
        return Cx4*W*(h/L)*(ax/g)
    else:
        raise ValueError; 't_no must be 1,2,3, or 4 (denotes tire number)'

def calc_lat_weight_transfer(ay,t_no):
    """
    Calculates lateral weight transfer

    Inputs:
    ay - lateral acceleration
    t_no - tire number

    Output:
    Weight transfer in N
    
    """
    #W needs to be W prime, see page 702 of Race Car Vehicle Dynamics
    #Wprime=
    if t_no ==1:
        return Cx1*W*(b_/L)
    elif t_no ==2:
        return Cx2*W*(b_/L)
    elif t_no==3:
        return Cx3*W*(a_/L)
    elif t_no==4:
        return Cx4*W*(a_/L)
    else:
        raise ValueError; 't_no must be 1,2,3, or 4 (denotes tire number)'


def calc_dyn_p(v):
    """
    Calculates dynamic pressure

    Inputs:
    v - velocity

    Outputs:
    q - dynamic pressure
    """
    return 1.23*.5*v**2

Cl = 2 #coef of lift (might need to be negative)
frontal_area = 1 #frontal area in m^2
Clf = 1 #coef of front lift
Clr = 1 #coef of rear lift 
### Could use rolling and pitching moment coefficients, however I do not have that data, thus we solve PM and RM with Clf, Clr, and Cl###

Kr = 6263.5101387 #rear roll rate in N-m/rad 
Kf = 30255.49782 #front roll rate in N-m/rad

def add_aero_loads(v,t_no):
    """ 
    Calculates aerodynamics load transfer for a certain tire

    Inputs:
    t_no - number of tire
    v - velocity

    Outputs:
    Weight transfer due to aero loads
    """
    q = calc_dyn_p(v)
    LF = Clf*q*frontal_area
    LR = Clr*q*frontal_area
    PM = (Clf-.5*Cl)*q*frontal_area*L
    RM = (.5*Cl-Clr)*q*frontal_area*L
    
    if t_no == 1:
        return (-LF*.5) - Kf/(Kf+Kr)*(RM/Tf)
    elif t_no == 2:
        return (-LF*.5) + Kf/(Kf+Kr)*(RM/Tf)
    elif t_no == 3:
        return (-LR*.5) - Kf/(Kf+Kr)*(RM/Tr)
    elif t_no == 4:
        return (-LR*.5) + Kf/(Kf+Kr)*(RM/Tr)
    else:
        raise ValueError  # 't_no must be 1,2,3, or 4 (denotes tire number)'
    

def calc_total_weight_transfer(ax, ay, v, t_no):
    """
    Calculates total weight transfer 

    Inputs:
    ax - longitudinal acceleration
    ay - lateral acceleration
    v - velocity 
    t_no = tire number

    Outputs:
    Added weight to a given tire in N
    """

    long = calc_long_weight_transfer(ax,t_no)
    lat = calc_lat_weight_transfer(ay,t_no)
    aero = add_aero_loads(v,t_no)
    return long+lat+aero
