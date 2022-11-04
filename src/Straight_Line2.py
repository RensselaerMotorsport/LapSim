import numpy as np
import math
import pandas as pd

from classes.car_simple import Car
from typing import List
# car_mass=195
# driver_mass=100
# frontal_area=1.54
# cd=1.41
# cl=2.77
# trans_efficiency=.9
# rho=1.23
# wheel_eff_r=.2032
# final_drive=6.0085
#
# gear_ratio=np.array([2.75,2,1.667,1.44])

rpm_torque = pd.read_csv("./data/rpm_torque.csv")
rm25 = Car("data/rm25.json")

rpms = rpm_torque.rpm.to_list()
torques = rpm_torque.torque.to_list()


def calc_road_speed(gear: int, rpm: int, car, transmission_efficiency: int = 0.9):
    """
    Finds road speed at a given RPM in a given gear as an integer 
    Gears- 0,1,2,3
    """
    final_drive = car.attrs["final_drive"]
    tire_radius = car.attrs["tire_radius"]
    gear_ratio = car.attrs["gear_ratio"][gear]

    return ((rpm / (final_drive * gear_ratio * transmission_efficiency) * 6) * 3.14) / 180 * tire_radius


def calc_torque(gear: int, torque: float, car, transmission_efficiency: int = 0.9):
    """Finds torque at wheels given a gear and torque"""
    final_drive = car.attrs["final_drive"]
    gear_ratio = car.attrs["gear_ratio"][gear]

    return torque * gear_ratio * final_drive * transmission_efficiency


def get_engine_force(gear: int, torque: float, car):
    """Finds engine force"""
    tire_radius = car.attrs["tire_radius"]

    return (calc_torque(gear, torque, car)) / tire_radius


def get_drag_force(velocity: float, car):
    """Calculates drag force given a velocity"""
    coeff_drag = car.attrs["Cd"]
    rho = car.attrs["rho"]
    frontal_area = car.attrs["A"]

    return velocity**2 * coeff_drag * .5 * rho * frontal_area


# def solve_v_f(v_i, seg_L, gr):
#     """Solves for final velocity of segment given in an initial velocity and segment length"""
#     x = get_engine_force()


def calc_corner_radius(coord1, coord2, coord3):
    """
    Calculates radius of corner at any given sector
    Coord1:Starting point of previous sector
    Coord2:Starting point of current sector
    Coord3:Starting point of next sector
    All inputs are in 1D two element numpy arrays
    """
    a = math.sqrt((coord3[1]-coord1[1])**2 + (coord3[2]-coord1[2])**2)
    b = math.sqrt((coord3[1]-coord2[1])**2 + (coord3[2]-coord2[2])**2)
    c = math.sqrt((coord2[1]-coord1[1])**2 + (coord2[2]-coord1[2])**2)
    return math.acos((b**2+c**2-a**2)/2*b*c)
