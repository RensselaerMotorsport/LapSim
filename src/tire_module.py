"""
COEFFICIENTS
 k: Spring constant (N/m)
 b: Damping coefficient (and Viscous Friction) (Ns/m)
 u: Coefficient of friction
 m: Mass (kg)
VARIABLES
 F: Force (N)
 x: Linear position (m)
 v: Linear velocity (m/s)
 a: Linear acceleration (m/s^2)
 α: Slip angle (rad)
 ω: Wheel speed (rad/s)
 SR: Slip ratio
"""
from math import cos
from math import sin

class Tire:
    def __init__(self, FN, α):
        self.k1 = 0.3 # Tire

        self.b1 = 0 # Tire

        self.u1 = 1.4 # Tire

        self.m1 = 4 # Tire

        self.FN = FN
        self.α = α
    def tf(self):
        Fx = FN * self.u1 * cos(self.α)
        Fy = FN * self.u1 * sin(self.α)
        return Fx, Fy
