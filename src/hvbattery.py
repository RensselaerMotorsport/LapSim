import numpy as np


class Cell():
    def __init__(self):
        self.vmax = 4.2  # Max voltage, V
        self.vmin = 2.5  # Min voltage, V
        self.dcr = 0.02 # DC resistance, Ohm
        self.c = 10.3 # Capacity, Wh
        self.e = self.c * 3600  # Energy, J
        self.m = 0.046 # Mass, kg
        self.cp = 900  # Special heat capacity, J/kgK

    def soev(self, v):
        return (v - self.vmin) / (self.vmax - self.vmin)

    def soee(self, e):
        return e / self.e

    def voc(self, e):
        return self.vmin + e / self.e * (self.vmax - self.vmin)

    def pwr_iter(self, na0, p, dt):
        na1 = np.zeros_like(na0)
        na1[0] = na0[0] + dt
        na1[8] = na0[8] - na0[7]
        na1[2] = self.voc(na1[8])
        na1[3] = self.dcr
        na1[6] = self.vmin * (na1[2] - self.vmin) / na1[3]
        na1[1] = min(p,na1[6])
        na1[4] = na1[2] / 2 / na1[3] - (na1[2] ** 2 / (4 * na1[3] ** 2) - p / na1[3]) ** 0.5
        if na1[4] != 0:
            na1[5] = p / na1[4]
        else:
            na1[5] = na1[2]
        # skip 6
        na1[7] = p * dt
        # skip 8
        na1[9] = self.soee(na1[8])
        na1[10] = na1[4] ** 2 * na1[3]
        na1[11] = na0[11] + na0[10] * dt
        na1[12] = na1[10] / (self.m * self.cp) * dt
        na1[13] = na0[13] + na0[12]
        return [na1]

    def pwr_cycle(self, p, T0, v0, t1, dt=0.0004):
        t = 0
        na = np.array([[0, 0, v0, self.dcr, 0, v0, self.vmin * (v0 - self.vmin) / self.dcr, 0, self.soev(v0) * self.e,
                        self.soev(v0), 0, 0, 0, T0]])
        # t, P, Voc, dcr, I, Vcc, PPk, dE, E, SOE, Qgen, Q, dT, T
        for i in range(p.size):
            t = 0
            while t < t1[i] + dt:
                na = np.append(na, self.pwr_iter(na[np.shape(na)[0]-1], p[i], dt),axis=0)
                t += dt
        return na
