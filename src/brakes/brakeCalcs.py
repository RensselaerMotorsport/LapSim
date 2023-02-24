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

#Master Cylinder Sizes
masterCylinderSizes = [5/8,7/10,3/4,13/16,7/8,15/16,1]

#User Input
def UserInput():
    """
    This function takes user input for the vehicle and brake system
    INPUTS: 
        none
    OUTPUTS:
        frontTireDiameter: diameter of front tires (in)
        rearTireDiameter: diameter of rear tires (in)
        frontWheelShellDiameter: diameter of front wheel shells (in)
        rearWheelShellDiameter: diameter of rear wheel shells (in)
        wheelbase: wheelbase of vehicle (in)
        forwardWeightDistribution: forward weight distribution of vehicle (in)
        centerOfGravityHeight: center of gravity height of vehicle (in)
        brakePedalRatio: brake pedal ratio of vehicle
        brakeBias: brake bias of vehicle
        frontMasterCylinder: front master cylinder size
        rearMasterCylinder: rear master cylinder size
        frontCaliper: front caliper
        rearCaliper: rear caliper
        frontPad: front pad
        rearPad: rear pad
        frontRotorOuter: front outer rotor
        frontRotorInner: front inner rotor
        rearRotorOuter: rear outer rotor
        rearRotorInner: rear inner rotor
    """

    # User inputs vehicle data
    frontTireDiameter = input("Please enter the diameter of your front tires in inches. ") #selects front tires 
    rearTireDiameter = input("Please enter the diameter of your rear tires in inches. ") #selects rear tires
    frontWheelShellDiameter = input("Please enter the diameter of your front wheel shells in inches. ") #selects front wheel shells
    rearWheelShellDiameter = input("Please enter the diameter of your rear wheel shells in inches. ") #selects rear wheel shells
    wheelbase = input("Please enter the wheelbase of your vehicle in inches. ") #selects wheelbase
    forwardWeightDistribution = input("Please enter the forward weight distribution of your vehicle in inches. ") #selects front weight distribution
    centerOfGravityHeight = input("Please enter the center of gravity height of your vehicle in inches. ") #selects center of gravity height
    
    # User inputs brake data
    brakePedalRatio = SelectBrakePedalRatio() #selects brake pedal ratio
    brakeBias = SelectBrakeBias() #selects brake bias
    frontMasterCylinder = SelectMasterCylinder(frontOrRear="front") #selects front master cylinder
    rearMasterCylinder = SelectMasterCylinder(frontOrRear="rear") #selects rear master cylinder
    frontCaliper = SelectCalipers(frontOrRear="front") #selects front calipers
    rearCaliper = SelectCalipers(frontOrRear="rear") #selects rear calipers
    frontPad = SelectPads(frontOrRear="front") #selects front pads
    rearPad = SelectPads(frontOrRear="rear") #selects rear pads
    
    frontRotorOuter, frontRotorInner = SelectRotors(frontOrRear="front") #selects front rotors
    rearRotorOuter, rearRotorInner = SelectRotors(frontOrRear="rear") #selects rear rotors

    #checks to see if pads and calipers are compatible with each other
    if (frontCaliper != -1 and frontPad != -1):
        if (caliperPadType[frontCaliper] != padType[frontPad]):
            print("Sorry, your front caliper (",caliperBrands[frontCaliper], caliperModel[frontCaliper],")and front pad(",padBrand[frontPad], padModel[frontPad],") are not compatible")
            return
    if (rearCaliper != -1 and rearPad != -1):
        if (caliperPadType[rearCaliper] != padType[rearPad]):
            print("Sorry, your rear caliper (",caliperBrands[rearCaliper], caliperModel[rearCaliper],")and rear pad(",padBrand[rearPad], padModel[rearPad],") are not compatible")
            return

    #checks to see if rotors are compatible with calipers
    if (frontCaliper != -1 and frontRotorOuter != -1):
        if (caliperMinRotorDiameter[frontCaliper] > frontRotorOuter*2):
            print("Sorry, your front caliper (",caliperBrands[frontCaliper], caliperModel[frontCaliper],")and front rotor outside radius (",frontRotorOuter,"in) are not compatible")
            return
    if (rearCaliper != -1 and rearRotorOuter != -1):
        if (caliperMinRotorDiameter[rearCaliper] > rearRotorOuter*2):
            print("Sorry, your rear caliper (",caliperBrands[rearCaliper], caliperModel[rearCaliper],")and rear rotor outside radius (",rearRotorOuter,"in) are not compatible")
            return

    #TBD: checks to see if rotors and calipers will fit inside the wheel shells

    return frontTireDiameter, rearTireDiameter, frontWheelShellDiameter, rearWheelShellDiameter, wheelbase, forwardWeightDistribution, centerOfGravityHeight, brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper, rearCaliper, frontPad, rearPad, frontRotorOuter, frontRotorInner, rearRotorOuter, rearRotorInner
        
#User Input Functions
def SelectCalipers(frontOrRear):
    """
    INPUTS: 
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        caliperNumber: int, the number of the caliper selected (can be used to refrence caliper data arrays). = -1 if no caliper is selected
    """
    #ask if user already has calipers selected
    print("\nPlease select your", frontOrRear, "calipers")
    haveCalipers = input("Have you chosen which calipers you will use? (y/n)")
    if haveCalipers == "y":
        print("Please enter the number corresponding to your", frontOrRear, "calipers")
        size = caliperBrands.size
        for n in range(size):
            print(n+1, ". Brand:",caliperBrands[n]," Model:", caliperModel[n], "Part Number:", caliperPartNumber[n])
        caliperNumber = int(input("if none of these match, please enter 0 \n"))
        if (caliperNumber > 0):
            caliperNumber = caliperNumber - 1
            print("You have selected", caliperBrands[caliperNumber], caliperModel[caliperNumber], "as your", frontOrRear, "calipers.")
        elif (caliperNumber==0):
            print("Sorry, you can not continue without a front caliper selection")
    else:
        print("Understood, a",frontOrRear,"caliper selection will be made for you")
        caliperNumber = -1
    return caliperNumber
def SelectPads(frontOrRear):
    """
    INPUTS:
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        padNumber: int, the number of the pad selected (can be used to refrence pad data arrays). = -1 if no pad is selected
    """
    print("\nPlease select your",frontOrRear, "pads")
    havePads = input("Have you chosen which pads you will use? (y/n)")
    if havePads == "y":
        print("Please enter the number corresponding to your", frontOrRear, "pads")
        size = padBrand.size
        for n in range(size):
            print(n+1, ". Brand:",padBrand[n]," Model:", padModel[n], "Part Number:", padPartNumber[n])
        padNumber = int(input("if none of these match, please enter 0 \n"))
        if (padNumber > 0):
            padNumber = padNumber - 1
            print("You have selected", padBrand[padNumber], padModel[padNumber], "for your", frontOrRear , "pads.")
        elif (padNumber==0):
            print("Sorry, you can not continue without a pad selection")
    else:
        print("Understood, a pad selection will be made for you")
        padNumber = -1
    return padNumber
def SelectMasterCylinder(frontOrRear):
    """
    INPUTS:
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        masterCylinderSize: float, the size of the master cylinder selected
    """
    print("\n")
    print("Please select your", frontOrRear, "master cylinder")
    haveMasterCylinder = input("Have you chosen which master cylinder you will use? (y/n)")
    if haveMasterCylinder == "y":
        print("Please enter the number corresponding to your", frontOrRear, "master cylinder")
        size = len(masterCylinderSizes)
        for n in range(size):
            print(n+1, ". Size:",masterCylinderSizes[n],"in")
        masterCylinderNumber = int(input("if none of these match, please enter 0 \n"))
        if (masterCylinderNumber > 0):
            masterCylinderNumber = masterCylinderNumber - 1
            masterCylinderSize = masterCylinderSizes[masterCylinderNumber]
            print("You have selected a", masterCylinderSize, "in master cylinder for your", frontOrRear, "hydraulic circut.")
        elif (masterCylinderNumber==0):
            print("Sorry, you can not continue without a master cylinder selection")
    else:
        print("Understood, a master cylinder selection will be made for you")
        masterCylinderSize = -1
    return masterCylinderSize
def SelectBrakePedalRatio():
    """
    INPUTS:
        none
    OUTPUTS:
        brakePedalRatio: float, the brake pedal ratio selected. If none is selected, brakePedalRatio = -1
    """
    print("\n")
    haveBrakePedalRatio = input("Do you know the brake pedal ratio of your vehicle? (y/n)") #checks to see if user knows brake pedal ratio
    if haveBrakePedalRatio == "y":
        brakePedalRatio = input("Please enter the brake pedal ratio of your vehicle.") #selects brake pedal ratio
    else:
        print ("Ok, a brake pedal ratio will be chosen for you")
        brakePedalRatio = -1
    return brakePedalRatio
def SelectBrakeBias():
    """
    INPUTS:
        none
    OUTPUTS:
        brakeBias: float, the brake bias selected. If none is selected, brakeBias = -1
    """
    print("\n")
    haveBrakeBias = input("Do you know the brake bias of your vehicle? (y/n)") #checks to see if user knows brake bias
    if haveBrakeBias == "y":
        brakeBias = input("Please enter the brake bias of your vehicle.") #selects brake bias
    else:
        print ("Ok, a brake bias will be chosen for you")
        brakeBias = -1
    return brakeBias
def SelectRotors(frontOrRear):
    """
    INPUTS:
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        rotorOuterRadius: float, the outer radius of the rotor selected. = -1 if no rotor size is selected
        rotorInnerRadius: float, the inner radius of the rotor selected. = -1 if no rotor size is selected
    """
    print("\nPlease select your", frontOrRear, "rotor size")
    haveRotors = input("Have you chosen what size rotors you will use? (y/n)")
    if haveRotors == "y":
        rotorOuterRadius = input("Please enter the outer radius of your rotors in inches. ")
        rotorInnerRadius = input("Please enter the inner radius of your rotors in inches. ")
    else:
        print("Understood, a rotor selection will be made for you")
        rotorOuterRadius, rotorInnerRadius = -1
    return rotorOuterRadius, rotorInnerRadius

UserInput()
