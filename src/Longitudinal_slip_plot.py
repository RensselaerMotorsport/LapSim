"""A module to calculate and plot slip angle and longitudinal force"""

# from Longitudinal_Slip import calc_longitudinal_wheel_slip
# from Longitudinal_Slip import calc_k

import matplotlib.pyplot as plt
import math 
import numpy as np


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

Fz = (m_car+m_driver)*g #neglects downforce!
D = Fz*(b1*Fz+b2)
C = b0
BCD = (b3*(Fz**2)+b4*Fz)*(math.e**(-b5*Fz)) #Stiffness
B = BCD/(C*D)
H = b9*Fz+b10

# print(Fz)
# print(D)
# print(C)
# print(BCD)
# print(B)
# print(H)


Sv_x = b11*Fz+b12

n = 20 #resolution

k = np.linspace(-1,1,n)

E = np.zeros(n)
Bc = np.zeros(n)
Fx = np.zeros(n)

for i in range(k.size):
    E[i] = (b6*(Fz**2)+b7*Fz+b8)*(1-b13*(math.sin((k[i]*100)+H)))
    Bc[i] = B*((k[i]*100) + H)
    
    Fx[i] = D*(math.sin(C*(math.atan(Bc[i]-E[i]*(Bc[i]-(math.atan(Bc[i]))))))) +Sv_x

print(k)
print(Fx)

plt.title("Slip Ratio vs Longitudinal Force")
plt.xlabel("Slip Ratio", fontsize = 14)
plt.ylabel("Longitudinal Force", fontsize = 14)
plt.xlim(-1,1)
plt.ylim(-2000000,2000000) #subject to change
plt.plot([Fx,k])
plt.show()



