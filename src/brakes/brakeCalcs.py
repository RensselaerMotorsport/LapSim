"""
BreakCalcs.py
This file contains the functions used to calculate the configuration of the braking system 
"""

import math 
import numpy as np
import timeit

#start timer to calculate total time to run program
start = timeit.default_timer()

"""Assumptions"""
#acceleration during braking is 1.1G (one tire compound, completly locked up)
#neglecting rotor thickness & temperature effects
#neglecting tire deformation
#assuming that the driver applies a constant force of 150lbs to the brake pedal

"""General Constants"""
acceleration = float(1.1) #acceleration during braking (G) and tire-ground coefficient of friction (mu)
diverPedalForce = float(150) #force applied by driver to brake pedal (lbs)
sampleSize = 10 #number of samples to take for each brake system configuration, can change to increase accuracy

#TBD: should I allow for multiple tire compounds?

"""Brake Constants"""
#imports caliper data from csv files into numpy arrays

#Brake Caliper Constants
caliperData = np.loadtxt(open("database - calipers.csv", "rb"), delimiter=",", skiprows=1, dtype=str)
caliperBrands = caliperData[:, [0]]
caliperModel = caliperData[:, [1]]
caliperPartNumber = caliperData[:, [2]]
caliperPistonArea = np.asarray(caliperData[:, [3]], dtype = float)
caliperNumberOfPistons = np.asarray(caliperData[:, [4]], dtype = float)
caliperWeight = np.asarray(caliperData[:, [5]], dtype = float)
caliperPrice = np.asarray(caliperData[:, [6]], dtype = float)
caliperMinRotorDiameter = np.asanyarray(caliperData[:, [7]], dtype = float)
caliperMaxRotorDiameter = np.asanyarray(caliperData[:, [8]], dtype = float)
caliperMinRotorThickness = np.asanyarray(caliperData[:, [9]], dtype = float)
caliperMaxRotorThickness = np.asanyarray(caliperData[:, [10]], dtype = float)
caliperPadType = caliperData[:, [11]]

#Brake Pad Constants
padData = np.loadtxt(open("database - pads.csv", "rb"), delimiter=",", skiprows=1, dtype=str)
padBrand = padData[:, [0]]
padModel = padData[:, [1]]
padPartNumber = padData[:, [3]]
padType = padData[:, [2]]
padArea = np.asarray(padData[:, [4]], dtype = float)
padCoefficientOfFrictionMin = np.asarray(padData[:, [5]], dtype = float)
padCoefficientOfFrictionMax = np.asarray(padData[:, [6]], dtype = float)
padIdealTemperature = padData[:, [7]]
padPricePer = np.asarray(padData[:, [8]], dtype = float)
padCompatableMaterial = padData[:, [9]]

#Master Cylinder Sizes
masterCylinderSizes = np.array([5/8,7/10,3/4,13/16,7/8,15/16,1])

#User Input

def UserInput():
    """
    This function takes user input for the vehicle and brake system
    INPUTS: 
        none
    OUTPUTS:
        vehicleWeight: weight of vehicle (lbs)
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
        frontRotorOuter: front outer rotor radius
        rearRotorOuter: rear outer rotor radius
        factorOfSafety: factor of safety for brake system
        priority: priority for brake system (cost, weight, performance)
    """
    
    #TBD: add priority as input: cost, weight, performance, etc.

    # User inputs vehicle data (required for all calculations)
    vehicleWeight = float(input("Please enter the weight of your vehicle (with driver) in pounds. ")) #selects vehicle weight
    frontTireDiameter = 2*float(input("Please enter the diameter of your front tires in inches. ")) #selects front tires 
    rearTireDiameter = 2*float(input("Please enter the diameter of your rear tires in inches. ")) #selects rear tires
    frontWheelShellDiameter = float(input("Please enter the diameter of your front wheel shells in inches. ")) #selects front wheel shells
    rearWheelShellDiameter = float(input("Please enter the diameter of your rear wheel shells in inches. ")) #selects rear wheel shells
    wheelbase = float(input("Please enter the wheelbase of your vehicle in inches. ")) #selects wheelbase
    forwardWeightDistribution = float(input("Please enter the forward weight distribution of your vehicle in inches. ")) #selects front weight distribution
    centerOfGravityHeight = float(input("Please enter the center of gravity height of your vehicle in inches. ")) #selects center of gravity height
    
    factorOfSafety = float(input("Please enter your desired factor of safety. ")) #selects factor of safety
    priority = float(input("Please enter your priority: cost(1), weight(2), or performance(3). ")) #selects priority
    
    # User inputs brake data
    brakePedalRatio = SelectBrakePedalRatio() #selects brake pedal ratio
    brakeBias = SelectBrakeBias() #selects brake bias
    frontMasterCylinder = SelectMasterCylinder(frontOrRear="front") #selects front master cylinder
    rearMasterCylinder = SelectMasterCylinder(frontOrRear="rear") #selects rear master cylinder
    frontCaliper = SelectCalipers(frontOrRear="front") #selects front calipers
    rearCaliper = SelectCalipers(frontOrRear="rear") #selects rear calipers
    frontPad = SelectPads(frontOrRear="front") #selects front pads
    rearPad = SelectPads(frontOrRear="rear") #selects rear pads

    # TBD: add min factor of safety

    #checks to see if pads and calipers are compatible with each other
    #TBD: make this an error message
    if (frontCaliper != -1 and frontPad != -1):
        if (caliperPadType[frontCaliper] != padType[frontPad]):
            print("Sorry, your front caliper (",caliperBrands[frontCaliper], caliperModel[frontCaliper],")and front pad(",padBrand[frontPad], padModel[frontPad],") are not compatible")
            return
    if (rearCaliper != -1 and rearPad != -1):
        if (caliperPadType[rearCaliper] != padType[rearPad]):
            print("Sorry, your rear caliper (",caliperBrands[rearCaliper], caliperModel[rearCaliper],")and rear pad(",padBrand[rearPad], padModel[rearPad],") are not compatible")
            return

    frontRotorOuter = SelectRotors(frontOrRear="front") #selects front rotors
    rearRotorOuter = SelectRotors(frontOrRear="rear") #selects rear rotors

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
    #TBD: ask for factor of safety (and get mad if it goes below)
    #TBD: add error checking for user input

    return vehicleWeight, frontTireDiameter, rearTireDiameter, frontWheelShellDiameter, rearWheelShellDiameter, wheelbase, forwardWeightDistribution, centerOfGravityHeight, brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper, rearCaliper, frontPad, rearPad, frontRotorOuter, rearRotorOuter, factorOfSafety, priority

#User Input Functions
def SelectCalipers(frontOrRear):
    """ Allows user to select calipers
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
    """ Allows user to select pads
    INPUTS:
        frontOrRear: string, either "front" or7- "rear"
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
            #TBD: make this an error message
    else:
        print("Understood, a pad selection will be made for you")
        padNumber = -1
    return padNumber

def SelectMasterCylinder(frontOrRear):
    """ Allows user to select a master cylinder
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
    """ Allows user to select a brake pedal ratio
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
    """ Allows user to select a brake bias
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
    """ Allows user to select rotor size
    INPUTS:
        frontOrRear: string, either "front" or "rear"
    OUTPUTS:
        rotorOuterRadius: float, the outer radius of the rotor selected. = -1 if 7no rotor size is selected
    """
    print("\nPlease select your", frontOrRear, "rotor size")
    haveRotors = input("Have you chosen what size rotors you will use? (y/n)")
    if haveRotors == "y":
        rotorOuterRadius = input("Please enter the outer radius of your rotors in inches. ")
    else:
        print("Understood, a rotor selection will be made for you")
        rotorOuterRadius = -1
    return rotorOuterRadius

#Brake System Calculations
def BrakeSystem(vehicleWeight, frontTireDiameter, rearTireDiameter, frontWheelShellDiameter, rearWheelShellDiameter, wheelbase, forwardWeightDistribution, centerOfGravityHeight, brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper, rearCaliper, frontPad, rearPad, frontRotorOuter, rearRotorOuter, factorOfSafety, priority):
    """ Calculates all possible brake system configurations
    INPUTS:
        vehicleWeight: float, the weight of the vehicle in lbs
        frontTireDiameter: float, the diameter of the front tires in inches
        rearTireDiameter: float, the diameter of the rear tires in inches
        frontWheelShellDiameter: float, the diameter of the front wheel shells in inches
        rearWheelShellDiameter: float, the diameter of the rear wheel shells in inches
        wheelbase: float, the wheelbase of the vehicle in inches
        forwardWeightDistribution: float, the forward weight distribution of the vehicle as a percentage
        centerOfGravityHeight: float, the height of the center of gravity of the vehicle in inches
        brakePedalRatio: float, the brake pedal ratio of the vehicle
        brakeBias: float, the brake bias of the vehicle
        frontMasterCylinder: float, the size of the front master cylinder in inches
        rearMasterCylinder: float, the size of the rear master cylinder in inches
        frontCaliper: float, the size of the front caliper in inches
        rearCaliper: float, the size of the rear caliper in inches
        frontPad: float, the number of the front pads in inches
        rearPad: float, the number of the rear pads in inches
        frontRotorOuter: float, the outer radius of the front rotor in inches
        rearRotorOuter: float, the outer radius of the rear rotor in inches
        factorOfSafety: float, the factor of safety of the brake system
        priority: float, the priority of the brake system (cost, weight, performance)
    OUTPUTS:
        TBD
    """
    
    requiredTorqueFront, requiredTorqueRear = RequiredTorque(wheelbase, frontTireDiameter, rearTireDiameter, vehicleWeight, forwardWeightDistribution, centerOfGravityHeight, acceleration)

    """ Setting Up Arrays Of Values To Iterate Through"""
    # if pedal ratio is not set by user
    if (brakePedalRatio == -1):
        #make 100 evenly spaced points between 1 and 10
        brakePedalRatios = np.linspace(5, 6, sampleSize)        
    else:
        brakePedalRatios = np.array([brakePedalRatio])
    
    # if front master cylinder is not set by user
    if (frontMasterCylinder == -1):
        frontMasterCylinderSizes = masterCylinderSizes
    else:
        frontMasterCylinderSizes = np.array([frontMasterCylinder])

    # if rear master cylinder is not set by user
    if (rearMasterCylinder == -1):
        rearMasterCylinderSizes = masterCylinderSizes
    else:
        rearMasterCylinderSizes = np.array([rearMasterCylinder])
    
    # if front caliper is not set by user
    if (frontCaliper == -1):
        # front caliper index array is set to the total number of possible calipers
        frontCaliperIndex = caliperPistonArea
    else:
        # front caliper index array is set to the user selected caliper
        frontCaliperIndex = np.array(caliperPistonArea[frontCaliper])
    
    # if rear caliper is not set by user
    if (rearCaliper == -1):
        # rear caliper index array is set to the total number of possible calipers
        rearCaliperIndex = caliperPistonArea
    else:
        # rear caliper index array is set to the user selected caliper
        rearCaliperIndex = np.array(caliperPistonArea[rearCaliper])

    # if front pads are not set by user
    if (frontPad == -1):
        frontPadIndex = padCoefficientOfFrictionMin
    else:
        frontPadIndex = np.array(padCoefficientOfFrictionMin[frontPad])
    
    # if rear pads are not set by user
    if (rearPad == -1):
        rearPadIndex = padCoefficientOfFrictionMin
    else: 
        rearPadIndex = np.array(padCoefficientOfFrictionMin[rearPad])
    
    # if front rotor size is not set by user
    if (frontRotorOuter == -1):
        frontRotorOuterRadises = np.linspace(np.min(caliperMinRotorDiameter)/2, np.max(caliperMaxRotorDiameter)/2, sampleSize)    
    else:
        frontRotorOuterRadises = np.array([frontRotorOuter])
    
    # if rear rotor size is not set by user
    if (rearRotorOuter == -1):
        rearRotorOuterRadises = np.linspace(np.min(caliperMinRotorDiameter)/2, np.max(caliperMaxRotorDiameter)/2, sampleSize)
    else:
        rearRotorOuterRadises = np.array([rearRotorOuter])

    """ Iterating Through All Possible Brake System Configurations """
    #frontPosibleCombinations = np.zeros((brakePedalRatios.size+1)*(frontMasterCylinderSizes.size+1)*(frontCaliperIndex+1)*(frontPadIndex+1)*(frontRotorOuterRadises.size+1))
    #rearPosibleCombinations = np.zeros((brakePedalRatios.size+1)*(rearMasterCylinderSizes.size+1)*(rearCaliperIndex+1)*(rearPadIndex+1)*(rearRotorOuterRadises+1))
    posibleCombinations = np.zeros((5000,15))
    i = 0

    idealBalance = requiredTorqueFront/requiredTorqueRear
    print("\n")
    
    
    #TBD, make more efficent by preventing repeat calculations
    #iterates through front and rear calipers and pads
    for c in range(frontCaliperIndex.size):
        for c1 in range(rearCaliperIndex.size):
            # resets difference for this hardware combination
            frontTorque = 0
            rearTorque = 0
            bestDifference = -1
            for d in range(frontPadIndex.size):
                #makes sure front pad and caliper are compatible 
                #front caliper is not set
                caseF1 = (frontCaliperIndex.size != 1) and ((padType[d] == caliperPadType[c]))
                #front caliper is  set
                caseF2 = (frontCaliperIndex.size == 1) and ((padType[frontPad] == caliperPadType[frontCaliper]))
                if (caseF1 or caseF2):
                    #iterates through rear calipers and pads
                    for d1 in range(rearPadIndex.size):
                        #makes sure rear pad and caliper are compatible 
                        #rear caliper not set
                        caseR1 = (rearCaliperIndex.size != 1) and ((padType[d1] == caliperPadType[c1]))
                        #rear caliper is set
                        caseR2 = (rearCaliperIndex.size == 1) and ((padType[rearPad] == caliperPadType[rearCaliper]))
                        if (caseR1 or caseR2):
                            #iterates through front master cylinders
                            for b in range(frontMasterCylinderSizes.size):
                                #iterates through rear cylinders
                                for b1 in range(rearMasterCylinderSizes.size):
                                    #iterates through front rotors
                                    for e in range(frontRotorOuterRadises.size):
                                        #TBD, make sure caliper isnt too small
                                        #checks if front rotors are compatible with caliper
                                        if ((2*frontRotorOuterRadises[e] <= caliperMaxRotorDiameter[c]) and (2*frontRotorOuterRadises[e] >= caliperMinRotorDiameter[c])):
                                            #iterates through rear rotors
                                            for e1 in range(rearRotorOuterRadises.size):
                                                #checks if rear rotors are compatible with caliper
                                                if ((2*rearRotorOuterRadises[e1] <= caliperMaxRotorDiameter[c1]) and (2*frontRotorOuterRadises[e1] >= caliperMinRotorDiameter[c1])):
                                                    #iterates through pedal ratios
                                                    for a in range(brakePedalRatios.size):
                                                        frontTorque = 0
                                                        rearTorque = 0
                                                        #checks if the torque is greater than the required torque and less than 2 times the required torque
                                                        frontTorque = TorqueAtCombination(brakePedalRatios[a],frontMasterCylinderSizes[b],frontCaliperIndex[c],frontPadIndex[d],frontRotorOuterRadises[e],caliperNumberOfPistons[c])
                                                        if (frontTorque >= requiredTorqueFront*factorOfSafety and frontTorque <= 2*requiredTorqueFront*factorOfSafety):
                                                            rearTorque = TorqueAtCombination(brakePedalRatios[a],rearMasterCylinderSizes[b1],rearCaliperIndex[c1],rearPadIndex[d1],rearRotorOuterRadises[e1],caliperNumberOfPistons[c1])
                                                            if (rearTorque >= requiredTorqueRear*factorOfSafety and rearTorque <= 2*requiredTorqueRear*factorOfSafety):
                                                                # checks if the torque balance is closer to the ideal balance than the previous best
                                                                if (abs((frontTorque/rearTorque) - idealBalance)<bestDifference  or bestDifference==-1):
                                                                    #record new best balance
                                                                    bestDifference = abs((frontTorque/rearTorque) - idealBalance)
                                                                    #record new best combination
                                                                    posibleCombinations[i,0] = (frontTorque)
                                                                    posibleCombinations[i,1] = (rearTorque)
                                                                    posibleCombinations[i,2] = brakePedalRatios[a] # record brake pedal rato
                                                                    posibleCombinations[i,3] = frontMasterCylinderSizes[b] # record front master cylinder size
                                                                    posibleCombinations[i,4] = rearMasterCylinderSizes[b1] # record rear master cylinder size
                                                                    if(frontCaliperIndex.size ==1):
                                                                        posibleCombinations[i,5] = frontCaliper 
                                                                    else:
                                                                        posibleCombinations[i,5] = c # record front caliper size
                                                                    if(rearCaliperIndex.size == 1):
                                                                        posibleCombinations[i,6] = rearCaliper
                                                                    else:
                                                                        posibleCombinations[i,6] = c1 # record rear caliper size
                                                                    if(frontPadIndex.size ==1):
                                                                        posibleCombinations[i,7] = frontPad # record front pad size
                                                                    else :
                                                                        posibleCombinations[i,7] = d
                                                                    if(rearPadIndex.size ==1):
                                                                        posibleCombinations[i,8] = rearPad # record rear pad size
                                                                    else:
                                                                        posibleCombinations[i,8] = d1

                                                                    posibleCombinations[i,9] = frontRotorOuterRadises[e] # record front rotor size
                                                                    posibleCombinations[i,10] = rearRotorOuterRadises[e1] # record rear rotor size
                                                                    posibleCombinations[i,11] = bestDifference
                                                                    posibleCombinations[i,12] = 100*bestDifference/idealBalance
                                                                    i+=1
            
            #if best difference is not the min for a calipers selection, delete the combination
            for j in range(posibleCombinations.shape[0]):
                if(frontCaliperIndex.size ==1):
                    if(posibleCombinations[j,6] == c1 or posibleCombinations[j,6]== rearCaliper):
                        if (posibleCombinations[j,11] != bestDifference):
                            posibleCombinations[j,:] = 0
                if(rearCaliperIndex.size ==1):
                    if(posibleCombinations[j,5] == c or posibleCombinations[j,5]== frontCaliper):
                        if (posibleCombinations[j,11] != bestDifference):
                            posibleCombinations[j,:] = 0
                if (posibleCombinations[j,5] == c and posibleCombinations[j,6] == c1):
                    if (posibleCombinations[j,11] != bestDifference):
                        posibleCombinations[j,:] = 0
                                                              
    """Filtering and Displaying Results"""      
    
    #delete duplicate entries and zeros
    posibleCombinations = np.unique(posibleCombinations, axis=0)    

    #delete first row if it is all zeros
    if (posibleCombinations[0,0] == 0):
        posibleCombinations = np.delete(posibleCombinations,0,0)

    #calculate total cost and weight of each combination
    for i in range(posibleCombinations.shape[0]):
        posibleCombinations[i,13] = 2*caliperPrice[int(posibleCombinations[i,5])] + 2*caliperPrice[int(posibleCombinations[i,6])] + 4*padPricePer[int(posibleCombinations[i,7])] + 4*padPricePer[int(posibleCombinations[i,8])]  #cost
        posibleCombinations[i,14] = 2*caliperWeight[int(posibleCombinations[i,5])] + 2*caliperWeight[int(posibleCombinations[i,6])] #weight

    #sort array by best percent off ideal balance
    if (priority==1): #cost
        posibleCombinations = posibleCombinations[posibleCombinations[:,13].argsort()]
    if (priority==2): #weight
        posibleCombinations = posibleCombinations[posibleCombinations[:,14].argsort()]
    if (priority==3): #performance
        posibleCombinations = posibleCombinations[posibleCombinations[:,12].argsort()]
    #print results sorted by best percent off ideal balance
    for i in range(posibleCombinations.shape[0]):
        print("Front Torque: ", posibleCombinations[i,0])
        print("Rear Torque: ", posibleCombinations[i,1])
        print("Brake Pedal Ratio: ", posibleCombinations[i,2])
        print("Front Master Cylinder Size: ", posibleCombinations[i,3])
        print("Rear Master Cylinder Size: ", posibleCombinations[i,4])
        print("Front Caliper: ", caliperBrands[int(posibleCombinations[i,5])]  , caliperModel[int(posibleCombinations[i,5])])
        print("Rear Caliper: ", caliperBrands[int(posibleCombinations[i,6])]  , caliperModel[int(posibleCombinations[i,6])])
        print("Front Pad: ", padBrand[int(posibleCombinations[i,7])] , padModel[int(posibleCombinations[i,7])])
        print("Rear Pad: ", padBrand[int(posibleCombinations[i,8])] , padModel[int(posibleCombinations[i,8])])
        print("Front Rotor Radius: ", posibleCombinations[i,9])
        print("Rear Rotor Radius: ", posibleCombinations[i,10])
        print("Percent off ideal balance: ", posibleCombinations[i,12])
        print("Total Cost: ", posibleCombinations[i,13])
        print("Total Weight: ", posibleCombinations[i,14] , "lbs")
        print("\n")   
    
    #print number of combinations
    print("Number of combinations: ", i+1)    
    

    return posibleCombinations


def RequiredTorque(wheelbase, frontTireDiameter, rearTireDiameter, vehicleWeight, forwardWeightDistribution, centerOfGravityHeight, acceleration):
    """ Calculates the required torque to lock the wheels
    INPUTS:
        frontTireDiameter: float, the diameter of the front tires in inches
        rearTireDiameter: float, the diameter of the rear tires in inches
        vehicleWeight: float, the weight of the vehicle in lbs
        forwardWeightDistribution: float, the forward weight distribution of the vehicle as a percentage
        centerOfGravityHeight: float, the height of the center of gravity of the vehicle in inches
        acceleration: float, the acceleration of the vehicle in g's
    OUTPUTS:
        requiredTorqueFront: float, the required torque to lock the front wheels in lbs-ft
        requiredTorqueRear: float, the required torque to lock the rear wheels in lbs-ft
    """
    weightTransfer = (centerOfGravityHeight * vehicleWeight * acceleration) / (wheelbase)
    normalLoadFront = ((vehicleWeight * forwardWeightDistribution) + weightTransfer)/2
    normalLoadRear = (vehicleWeight - (2*normalLoadFront))/2
    requiredTorqueFront = 2*(frontTireDiameter/2)*normalLoadFront*acceleration
    requiredTorqueRear = 2*(rearTireDiameter/2)*normalLoadRear*acceleration
    print("\nYour vehicle will reqire", requiredTorqueFront, "lbs-ft of front braking torque to lock the wheels.")
    print("Your vehicle will reqire", requiredTorqueRear, "lbs-ft of rear braking torque to lock the wheels.")
    return requiredTorqueFront, requiredTorqueRear

def TorqueAtCombination(brakePedalRatio, masterCylinderSize, caliperPistonArea, padCoefficientOfFrictionMax, rotorRadiusOuter, numberOfPistons):
    """ Calculates the max torque with a combination of components
    INPUTS:
        brakePedalRatio: float, the ratio of the brake pedal to the master cylinder
        masterCylinderSize: float, the size of the master cylinder in inches
        caliperSize: float, the size of the caliper in inches
        padCoefficientOfFrictionMax: float, the coefficient of friction of the pads
        rotorRadiusOuter: float, the outer radius of the rotor in inches
        caliperPistonArea: float, the area of the caliper piston in inches^2
    OUTPUTS:
        torque: float, the torque at the combination. 
    """
    rotorEffectiveRadius = rotorRadiusOuter - math.sqrt(caliperPistonArea/math.pi)
    masterCylinderArea = math.pi*(masterCylinderSize**2)
    linePressure = (diverPedalForce*(brakePedalRatio/2))/(masterCylinderArea/2)
    torque = numberOfPistons * padCoefficientOfFrictionMax * rotorEffectiveRadius * caliperPistonArea * linePressure 

    return torque

#Calculating all RM26 Possible Combinations
BrakeSystem(700, 8, 8, 10, 10, 60.5, 0.49, 13, 5.25, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1.3, 2)

#TBD: Calculating RM26 Master Cylinder Size (broken)
#BrakeSystem(600, 8, 8, 10, 10, 60.5, 0.49, 13, 5.25, -1, -1, -1 , 2, -1, -1, -1, 8/2, 7.5/2, 1.0, 3)

#brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper, rearCaliper, frontPad, rearPad, frontRotorOuter, rearRotorOuter, factorOfSafety, priority

#BrakeSystem(vehicleWeight, frontTireDiameter, rearTireDiameter, frontWheelShellDiameter, rearWheelShellDiameter, wheelbase, forwardWeightDistribution, centerOfGravityHeight, brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper, rearCaliper, frontPad, rearPad, frontRotorOuter, rearRotorOuter, factorOfSafety)

stop = timeit.default_timer()
print('Time: ', stop - start)  