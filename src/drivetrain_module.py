import matplotlib.pyplot as plt
import numpy as np


class Drivetrain:
    def __init__(self):
        # J: Inertia (kgm^2)
        # k: Spring constant (N/m)
        # b: Damping coefficient (and Viscous Friction) (Ns/m)
        # N: Number of teeth
        # r: Radius (m)
        J1 = 0.02521  # Motor
        J2a = 0.0001141295  # Motor Cover shaft
        J2b = 0.0000632043  # Motor Internal shaft
        J2 = J2a + J2b  # Motor Shaft (Currently not including bolts, washers, circlip, spacer, cotter pin, castle nut, or bearing)
        J3 = 0.0000228259  # Motor Sprocket
        J4 = 0  # Chain
        J5a = 0.0019226425  # Diff Sprocket
        J5b = 0.000155099  # Sprocket Adapter
        J5 = J5a + J5b  # Diff Sprocket (Currently not including bolts, washers,
        J6 = 0  # Differential
        J7 = 0.0000556015  # Right Half-shaft
        J8 = 0  # Left Half-shaft
        J9 = J1  # Wheel

        k1 = 0  # Chain

        b1 = 0  # Motor
        b2 = 0  # Chain
        b3 = 0  # Differential
        b4 = 0  # Tripod

        N1 = 42  # Motor sprocket
        N2 = 12  # Diff sprocket

        r1 = 0.05306809079 / 2  # Motor sprocket
        r2 = 0.1941806998 / 2  # Diff sprocket
        r3 = 0.2032  # Wheel

    def transfer_function(self, Tmotor, ωwheel):
        # T: Torque (Nm)
        # θ: Angular position (rad)
        # ω: Angular velocity (rad/s)
        # α: Angular acceleration (rad/s^2)
        # F: Force (N)
        # x: Linear position (m)
        # v: Linear velocity (m/s)
        # a: Linear acceleration (m/s^2)
        T1 = Tmotor  # Motor input
        ω4 = ωwheel  # Whee speed input
        F1 = (T1 * r2 * (J6 + J7 + J9)) / (r2 * r1 * (J1 + J2) + r2 * r2 * (J6 + J7 + J9))
        α1 = (T1 - F1 * r1) / (J1 + J2)
        α4 = α1 * r2 / r1
        return α4

Tin = 230
w = 0
print(Drivetrain.transfer_function(0,Tin,w) * r3)
print(Tin * N2 / N1 / r3)
