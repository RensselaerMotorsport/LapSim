"""A script to model longitudinal wheel slip using the magic tire formula"""

import math 


#Initial Parameters 

b0 = 1.5  #Shape Factor - typical range = 1.4...1.8
b1 = 0    #Load influence on longitudinal friction coefficient(*100) 1/kN - typical range = -80...+80 
b2 = 1100 #Longitudinal friction coefficient (*1000) - typical range = 900...1700
b3 = 0    #Curvature factor of stiffness/load N/%/kN^2  - typical range = -20...+20
b4 = 300  #Change of stiffness with slip N/% - typical range = 100...500
b5 = 0    #Change of progressivity of stiffness/load 1/kN - typical range = -1...+1
b6 = 0    #Curvature change with load^2 - typical range = -.1...+.1
b7 = 0    #Curvature change with load - typical range = -1...+1
b8 = -2   #Curvature factor - typical range = -20...+1
b9 = 0    #Load influence on horizontal shift %/kN - typical range = -1...+1 
b10 = 0   #Horizontal shift % - typical range = -5...+5
b11 = 0   #Vertical shift N - typical range = -100...+100
b12 = 0   #Vertical shift at zero load N - typical range = -10...+10
b13 = 0   #Curvature shift - typical range = -1...+1
m_car = 195 #kg
m_driver = 100 #kg
g = 9.81 #m/s**2
Re = .2032 #m


Fz = (m_car+m_driver)*g #neglets downforce!
D = Fz*(b1*Fz+b2)
C = b0
BCD = (b3*Fz**2+b4*Fz)*math.e**(-b5*Fz) #Stiffness
B = BCD/(C*D)
H = b9*Fz+b10
E = (b6*Fz**2+b7*Fz+b8)*(1-b13*math.sin(k+H))
Sv_x = b11*Fz+b12
Bc = B*(k+H)




def calc_longitduinal_wheel_slip(D, C, B, E, Sv_x, k):
    """
    Inputs:
    D - Peak Factor 
        Determines the maximum value of Fx
    C - Shape factor 
        Describes the tire deformation
    B - Stiffness Factor
        Describes the longitudinal slip stiffness
    E - Curvature factor
        Changes the behavior of the longtudinal slip stiffness beyond the critical slip
    Sv_x - 
        Affects that account for rolling resistance or tire asymmetry
    k - Slip ratio

    Outputs:
    Fx (always positive) - longitudinal force
    """

    Fx = D*math.sin(C*math.arctan(Bc-E*(Bc-math.arctan(Bc)))) +Sv_x


def calc_k(Vx, Re):
    """
    Inputs:
    Vx - Longitudinal velocity in m/s
         Cheese using a tiny initial V
    Re - Wheel effective radius in m

    Outputs:
    k - slip ratio
    """
    
    omega = Vx/Re
    k = (Vx-(Re*omega))/Vx
    
    


#all magic coeff except C rely on Fz, the nominal tire load
