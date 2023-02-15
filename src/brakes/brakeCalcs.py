"""
BreakCalcs.py
This file contains the functions used to calculate the configuration of the braking system 
"""

from math import pi
# import matplotlib.pyplot as plt
import numpy as np
import csv 


"""Vehicle Constants"""
wd= 0.49 # front weight distribution: guestimate from Michael
a = 1.1 #acceleration during braking: taken from RM25 brake test data (G)
Pf = 1165 #max line pressure front: from RM25 data (PSI)
Pr = 787 #max line pressure rear: from RM25 data (PSI)
RR = 3.223 #rotor radius: effective, for 8" rotor (in)
R = 8 #tire radius (in)
h = 13.0 #CG height: Jasper & Michael's guestimate (in)
WB = 60.5 #wheelbase length, in, Michael & Jasper's Guestimate

"""Brake Constants"""
#imports caliper data from csv files into numpy array

#Brake Caliper Constants
caliperData = np.loadtxt(open("database - calipers.csv", "rb"), delimiter=",", skiprows=1, dtype=str)
caliperBrands = caliperData[:, [0]]
caliperModel = caliperData[:, [1]]
caliperPartNumber = caliperData[:, [2]]
caliperPartNumber = caliperData[:, [3]]
caliperPistonArea = np.asarray(caliperData[:, [4]], dtype = float)
caliperWeight = np.asarray(caliperData[:, [5]], dtype = float)
caliperPrice = np.asarray(caliperData[:, [6]], dtype = float)
caliperMinRotorDiameter = caliperData[:, [7]]
caliperMaxRotorDiameter = caliperData[:, [8]]
caliperMinRotorThickness = caliperData[:, [9]]
caliperMaxRotorThickness = caliperData[:, [10]]
caliperPadType = caliperData[:, [11]]

#Brake Pad Constants
padData = np.loadtxt(open("database - pads.csv", "rb"), delimiter=",", skiprows=1, dtype=str)
padBrand = padData[:, [0]]
padModel = padData[:, [1]]
padType = padData[:, [2]]
padPartNumber = padData[:, [3]]
padArea = np.asarray(padData[:, [4]], dtype = float)
padCoefficientOfFrictionMin = np.asarray(padData[:, [5]], dtype = float)
padCoefficientOfFrictionMax = np.asarray(padData[:, [6]], dtype = float)
padIdealTemperature = np.asarray(padData[:, [7]], dtype = float)
padPricePer = padData[:, [8]]
padCompatableMaterial = padData[:, [9]]

#User Input
def UserInput():
    frontCaliper = SelectCalipers(frontOrRear="front") #selects front calipers
    rearCaliper = SelectCalipers(frontOrRear="rear") #selects rear calipers
    #ask if user already has front calipers selected

def SelectCalipers(frontOrRear):
    """
    INPUTS: 
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        caliperNumber: int, the number of the caliper selected (can be used to refrence caliper data arrays). = -1 if no caliper is selected
    """
    #ask if user already has calipers selected
    print("Please select your", frontOrRear, "calipers")
    haveCalipers = input("Do you already have calipers selected? (y/n)")
    if haveCalipers == "y":
        print("Please enter the number correytspoding to your front calipers")
        size = caliperBrands.size
        for n in range(size):
            print(n+1, ". Brand:",caliperBrands[n]," Model:", caliperModel[n], "Part Number:", caliperPartNumber[n])
        caliperNumber = int(input("if none of these match, please enter 0 \n"))
        if (caliperNumber > 0):
            caliperNumber = caliperNumber - 1
            print("You have selected", caliperBrands[caliperNumber], caliperModel[caliperNumber])
        elif (caliperNumber==0):
            print("Sorry, you can not continue without a front caliper selection")
    else:
        print("Understood, a",frontOrRear,"caliper selection will be made for you")
        caliperNumber = -1
    return caliperNumber

UserInput()
