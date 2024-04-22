class Drivetrain:
    def __init__(self, Tmotor, ωwheel):
        # J: Inertia (kgm^2)
        # k: Spring constant (N/m)
        # b: Damping coefficient (and Viscous Friction) (Ns/m)
        # N: Number of teeth
        # r: Radius (m)
        self.J1 = 0.02521  # Motor
        self.J2a = 0.0001141295  # Motor Cover shaft
        self.J2b = 0.0000632043  # Motor Internal shaft
        self.J2 = self.J2a + self.J2b  # Motor Shaft (Currently not including bolts, washers, circlip, spacer, cotter pin, castle nut, or bearing)
        self.J3 = 0.0000228259  # Motor Sprocket
        self.J4 = 0  # Chain
        self.J5a = 0.0019226425  # Diff Sprocket
        self.J5b = 0.000155099  # Sprocket Adapter
        self.J5 = self.J5a + self.J5b  # Diff Sprocket (Currently not including bolts, washers,
        self.J6 = 0  # Differential
        self.J7 = 0.0000556015  # Right Half-shaft
        self.J8 = 0  # Left Half-shaft
        self.J9 = self.J1  # Wheel

        self.k1 = 0  # Chain

        self.b1 = 0  # Motor
        self.b2 = 0  # Chain
        self.b3 = 0  # Differential
        self.b4 = 0  # Tripod

        self.N1 = 42  # Motor sprocket
        self.N2 = 12  # Diff sprocket

        self.r1 = 0.05306809079 / 2  # Motor sprocket
        self.r2 = 0.1941806998 / 2  # Diff sprocket
        self.r3 = 0.2032  #

        self.T1 = Tmotor
        self.ω4 = ωwheel

    def transfer_function(self):
        # T: Torque (Nm)
        # θ: Angular position (rad)
        # ω: Angular velocity (rad/s)
        # α: Angular acceleration (rad/s^2)
        # F: Force (N)
        # x: Linear position (m)
        # v: Linear velocity (m/s)
        # a: Linear acceleration (m/s^2)
        F1 = (self.T1 * self.r2 * (self.J6 + self.J7 + self.J9)) / (self.r2 * self.r1 * (self.J1 + self.J2) + self.r2 * self.r2 * (self.J6 + self.J7 + self.J9))
        α1 = (self.T1 - F1 * self.r1) / (self.J1 + self.J2)
        α4 = α1 * self.r2 / self.r1
        T4 = α4 * (self.J6 + self.J7 + self.J9 + (self.N2 / self.N1) ** 2 * (self.J1 + self.J2))
        print(T4)
        return T4

Tin = 230
w = 0

Drivetrain(Tin,w).transfer_function()
print(Tin * 42 / 12)
