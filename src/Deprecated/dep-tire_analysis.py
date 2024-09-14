"""
GOALS:
Interpret TTC data
Produce tire plots (additional plots for tire pressure)
 - Lateral Force (FY) vs. Slip Angle (SA)
 - Lateral Force (FY) vs. Tire Temperature (T) vs. Slip Angle (SA)
 - Aligning Torque (MZ) vs. Slip Angle (SA)
 - Lateral Force (FY) vs. Normal Force (FZ) - load sensitivity
 - FY vs. SR
 - RM26: https://docs.google.com/document/d/1RiBCi_AwGDYZcIdQq6tsntvr8MlopEIcqNSumrCd7W0/edit
 - RM26: https://docs.google.com/document/d/1vXJgkuCZN1qB4e_nFj_hRyvR1lSjqEdBzcHVih0J7Bg/edit
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import isclose
import os


class TireData:
    def __init__(self, filedir):
        df = pd.read_table(filedir,sep='	',skiprows=[0,2])
        self.ET = np.array(df.loc[:,'ET'])
        self.V = np.array(df.loc[:, 'V'])
        self.N = np.array(df.loc[:, 'N'])
        self.SA = np.array(df.loc[:, 'SA'])
        self.IA = np.array(df.loc[:, 'IA'])
        self.RL = np.array(df.loc[:, 'RL'])
        self.RE = np.array(df.loc[:, 'RE'])
        self.P = np.array(df.loc[:, 'P'])
        self.FX = np.array(df.loc[:, 'FX'])
        self.FY = np.array(df.loc[:, 'FY'])
        self.FZ = np.array(df.loc[:, 'FZ'])
        self.MX = np.array(df.loc[:, 'MX'])
        self.MZ = np.array(df.loc[:, 'MZ'])
        self.NFX = np.array(df.loc[:, 'NFX'])
        self.NFY = np.array(df.loc[:, 'NFY'])
        self.RST = np.array(df.loc[:, 'RST'])
        self.TSTI = np.array(df.loc[:, 'TSTI'])
        self.TSTC = np.array(df.loc[:, 'TSTC'])
        self.TSTO = np.array(df.loc[:, 'TSTO'])
        self.AMBTMP = np.array(df.loc[:, 'AMBTMP'])
        self.SR = np.array(df.loc[:, 'SR'])
    def plot_FY_SA(self):
        plt.figure(figsize=(16, 9))
        fig, (ax1,ax2) = plt.figure()
        fig.tight_layout()
        #ax = fig.add_subplot(1, 1, 1)
        ax.grid()
        #fig.xlim(-15,15)
        #fig.ylim(-3000,3000)

        ax.plot(self.SA,self.FY,)
        fig.suptitle('Suptitle')
        ax.set_title('Title')
        fig.xlabel("Slip Angle, SA (deg)")
        #fig.ylabel("Lateral Force, FY (N)")
        fig.show()


R0 = TireData('RawData_DriveBrake_ASCII_SI/B1464run28.dat')
R0.plot_FY_SA()





"""
Analysis of Tire data from Motec
"""

# NAME = 'Endurance Traction Data.csv'
NAME1 = 'S1_#6520_20220618_113723.csv'
NAME2 = 'S2_#6520_20220618_113723.csv'

DATA1 = pd.read_csv(NAME1, on_bad_lines='skip',skiprows=[1])
DATA1 = DATA1.to_numpy()
DATA1 = DATA1.tolist()

DATA2 = pd.read_csv(NAME2, on_bad_lines='skip',skiprows=[1])
DATA2 = DATA2.to_numpy()
DATA2 = DATA2.tolist()

t1 = []
v1 = []
o1 = []
a1 = []
for i in DATA1:
    t1.append(i[0])
    v1.append(i[1])
    o1.append(-i[2])
    a1.append(i[3])

t2 = []
v2 = []
o2 = []
a2 = []
for i in DATA2:
    t2.append(i[0])
    v2.append(i[1])
    o2.append(-i[2])
    a2.append(i[3])


def mv_avg(arr):
    moving_averages = []
    window_size = 5
    i = 0

    # Loop through the array to consider
    # every window of size 3
    while i < len(arr) - window_size + 1:
        # Store elements from i to i+window_size
        # in list to get the current window
        window = arr[i: i + window_size]

        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)

        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)

        # Shift window to right by one position
        i += 1
    return moving_averages


def plot(x,y,z):
    fig = plt.figure(figsize=(9.6,7.2))
    ax = fig.add_subplot(projection='3d')
    #ax.set_axisbelow(True)
    ax.grid()
    ax.scatter(x,y,z)
    ax.set_xlabel('Long')
    ax.set_ylabel('Lat')
    ax.set_zlabel('Vel')
    ax.set_title("RM25 Endurance GG plot")
    fig.tight_layout()
    plt.show()

#plot(o1,a1,v1)


def find_max(x,y):
    X,Y = [],[]
    for i in range(len(x)):
        if x[i] in X:
            j = X.index(x[i])
            if y[j] > Y[j]:
                Y[j] = y[j]
        else:
            X.append(x[i])
            Y.append(y[i])
    return X,Y

def return_max(x,y,xval,tol=0.5):
    Y = []
    for i in range(len(x)):
        if isclose(x[i], xval,rel_tol=tol):
            Y.append(y[i])
    return min(Y)

#print(return_max(v1,o1,0))
#print(return_max(v2,o2,0,tol=1))

#plt.scatter(v2,o2)
#for i in range(len(v1)): v1[i] = v1[i] / 30
#plt.scatter(t1,o1)
#plt.scatter(t1,v1)
#plt.xlim(0,5)
#plt.ylim(0,2)
#plt.grid()
#plt.show()

#vM, oM = find_max(v2,o2)
#plt.plot(vM, oM)
#plt.xlim(0,60)
#plt.ylim(0,2.5)
#plt.show()


print(return_max(v2,o2,50,tol=50))

fig = plt.figure(figsize=(9.6,7.2))
ax = fig.add_subplot()
ax.scatter(a2,o2,s=350)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_xlabel("Lateral accel (g's)")
ax.set_ylabel("Longitudinal accel (g's)")
ax.grid()
ax.set_axisbelow(True)
ax.set_title("RM25 g-g Diagram")
fig.tight_layout()
plt.show()






#O2 = [0]
#for i in range(1,len(v2)):
#    if abs((v2[i] - v2[i-1]) / (0.02 * 2.237 * 9.81)) < 2:
#        O2.append((v2[i] - v2[i-1]) / (0.02 * 2.237 * 9.81))
#    else: O2.append(0)

#plt.scatter(t2,o2,s=25,label="Acceleration")
#plt.show()

#plt.plot(t2,O2,label="Derivative")
#plt.show()


#vM, oM = find_max(v2,o2)
#plt.scatter(vM, oM)
#plt.show()


#print(len(x))
#print("Max Lat: " + str(max(x)))
#print("Min Lat: " + str(min(x)))
#print("Max Lon: " + str(max(y)))
#print("Min Lon: " + str(min(y)))
