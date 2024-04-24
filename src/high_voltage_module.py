"""
ASSUME dI/dt = 0
COEFFICIENTS
 R: Resistance (Ohm)
 L: Inductance (H)
 Kb: Induced Voltage Constant (VRMS*s/rad)
VARIABLES
 V: Voltage (V)
 I: Current (A)
 ω: Angular velocity (rad/s)
"""
from math import pi

class HighVoltage:
    def __init__(self, VBat, Ibat, ωmotor):
        self.R1 = 3 * 0.01548 # Motor Internal resistance

        self.L1 = 3 * 225.5E-6 # Motor phase inductance

        self.Kb = 1 / 10.14 # Inverse of motor KV OR Induced voltage?

        self.V1 = VBat
        self.Ibat = Ibat
        self.ω1 = ωmotor

    def tf(self):
        s = 0
        V1 = self.V1 - self.Kb * self.ω1 * (2 * pi) / 60
        I1 = (self.V1 - self.Kb * self.ω1 * (2 * pi) / 60) / (s * self.L1 + self.R1)
        P1 = V1 * I1
        if I1 > self.Ibat: I1 = self.Ibat
        if I1 < 0: I1 = 0
        return I1