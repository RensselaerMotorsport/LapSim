"""
BreakCalcs.py
This file contains the functions used to calculate the configuration of the braking system 
"""

from math import pi
import matplotlib.pyplot as plt
import numpy as np

"""Definining Constants"""
wd= 0.49 # front weight distribution: guestimate from Michael
a = 1.1 #acceleration during braking: taken from RM25 brake test data (G)
Pf = 1165 #max line pressure front: from RM25 data (PSI)
Pr = 787 #max line pressure rear: from RM25 data (PSI)
RR = 3.223 #rotor radius: effective, for 8" rotor (in)
R = 8 #tire radius (in)
h = 13.0 #CG height: Jasper & Michael's guestimate (in)
WB = 60.5 #wheelbase length, in, Michael & Jasper's Guestimate
A_22_049 = (((0.984252/2)**2)*pi) #ISR 22-049 piston area (in^2)
A_GP200 = 1.23  #Wilwood GP200 piston area (in^2)
u_22_049 = 0.45 #coeficent of friction between ISR 22-059 pad & rotor: obtained from ISR
u_GP200 = 0.5 #coeficent of friction between Wilwood GP200 pad & rotor: obtained from Wilwood
u_TG = 1.1 #coeficent of friction between tire and ground, g, stolen shamelessly from Zips' design report