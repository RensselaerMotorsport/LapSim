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