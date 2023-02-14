"""Acceleration event calculation."""

import math
from helper_functions_ev.py import calc_vmax
from helper_functions_ev import straightlinesegment

def run_accel(car):
    return straightlinesegment(car, 75, vinitial= 0.001)
