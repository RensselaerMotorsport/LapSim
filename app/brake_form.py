from brakeCalcs import BrakeSystem

# User Input
def brake_input(car):
    vehicleWeight = float(car.attrs["vehicle_weight"])
    frontTireDiameter = float(car.attrs["front_tire_diameter"])
    rearTireDiameter = float(car.attrs["rear_tire_diameter"])
    frontWheelShellDiameter = float(car.attrs["front_wheel_shell_diameter"])
    rearWheelShellDiameter = float(car.attrs["rear_wheel_shell_diameter"])
    wheelbase = float(car.attrs["wheelbase"])
    forwardWeightDistribution = float(car.attrs["forward_weight_distribution"])
    centerOfGravityHeight = float(car.attrs["center_of_gravity_height"])
    brakePedalRatio = float(car.attrs["brake_pedal_ratio"])
    brakeBias = float(car.attrs["brake_bias"])
    frontMasterCylinder = float(car.attrs["front_master_cylinder"])
    rearMasterCylinder = float(car.attrs["rear_master_cylinder"])
    frontCaliper = int(car.attrs["front_caliper"])
    rearCaliper = int(car.attrs["rear_caliper"])
    frontPad = int(car.attrs["front_pad"])
    rearPad = int(car.attrs["rear_pad"])
    frontRotorOuter = float(car.attrs["front_rotor_outer"])
    rearRotorOuter = float(car.attrs["rear_rotor_outer"])
    factorOfSafety = float(car.attrs["factor_of_safety"])
    priority = int(car.attrs["priority"])

    return BrakeSystem(vehicleWeight, frontTireDiameter, rearTireDiameter, frontWheelShellDiameter,
                       rearWheelShellDiameter, wheelbase, forwardWeightDistribution, centerOfGravityHeight,
                       brakePedalRatio, brakeBias, frontMasterCylinder, rearMasterCylinder, frontCaliper,
                       rearCaliper, frontPad, rearPad, frontRotorOuter, rearRotorOuter, factorOfSafety, priority)