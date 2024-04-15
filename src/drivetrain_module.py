import matplotlib.pyplot as plt
import numpy as np



# J: Inertia (kgm^2)
# k: Spring constant (N/m)
# b: Damping coefficient (and Viscous Friction) (Ns/m)
# N: Number of teeth
# r: Radius (m)


J1 = 0.02521 # Motor
J2 = 0.001 # Motor Shaft
J3 = 0.001 # Motor Sprocket
J4 = 0.001 # Chain
J5 = 0.001 # Diff Sprocket
J6 = 0.001 # Differential
J7 = 0.001 # Right Half-shaft
J8 = 0.001 # Left Half-shaft
J9 = 0.001 # Wheel

k1 = 1 # Chain

b1 = 0.001 # Motor
b2 = 0.001 # Chain
b3 = 0.001 # Differential
b4 = 0.001 # Tripod
b5 = 0.001 # Wheel

N1 = 42 # Motor sprocket
N2 = 12 # Diff sprocket

r1 = 1 # Motor sprocket
r2 = 1 # Diff sprocket
r3 = 0.2032 # Wheel




# T: Torque (Nm)
# θ: Angular position (rad)
# ω: Angular velocity (rad/s)
# α: Angular acceleration (rad/s^2)
# F: Force (N)
# x: Linear position (m)
# v: Linear velocity (m/s)
# a: Linear acceleration (m/s^2)

def transfer_function(Tmotor, ωmotor, θmotor):
    T1 = Tmotor # Motor input
