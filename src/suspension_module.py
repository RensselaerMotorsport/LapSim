"""
COEFFICIENTS
 J: Inertia (kgm^2)
 k: Spring constant (N/m)
 b: Damping coefficient (and Viscous Friction) (Ns/m)
 N: Number of teeth
 r: Radius (m)
 KT: Motor torque constant (Nm/ARMS)
VARIABLES
 T: Torque (Nm)
 θ: Angular position (rad)
 ω: Angular velocity (rad/s)
 α: Angular acceleration (rad/s^2)
 F: Force (N)
 x: Linear position (m)
 v: Linear velocity (m/s)
 a: Linear acceleration (m/s^2)
"""
class Suspension:
    def __init__(self):
        self.k1 = 0
        # Will involve many springs, dampers, and forces
        # Need to use wheelbase, track width, etc

    def tf(self):
        # Will involve load calculations, load transfer, and overall vehicle characteristics
        return
