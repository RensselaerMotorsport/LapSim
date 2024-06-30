import numpy as np
import matplotlib.pyplot as plt



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

    def soee(self,e):
        return e / self.e

    def voc(self,e):
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
        na1[5] = p / na1[4]
        # skip 6
        na1[7] = p * dt
        # skip 8
        na1[9] = self.soee(na1[8])
        na1[10] = na1[4] ** 2 * na1[3]
        na1[11] = na0[11] + na0[10]
        na1[12] = na1[10] / (self.m * self.cp)
        na1[13] = na0[13] + na0[12]
        return [na1]

    def pwr_cycle(self, p, T0, v0, t1, dt=1):
        t = 0
        na = np.array([[0, 0, v0, self.dcr, 0, v0, self.vmin * (v0 - self.vmin) / self.dcr, 0, self.soev(v0) * self.e, self.soev(v0), 0, 0, 0, T0]])
        # t, P, Voc, dcr, I, Vcc, PPk, dE, E, SOE, Qgen, Q, dT, T
        while t < t1 + dt:
            na = np.append(na, self.pwr_iter(na[np.shape(na)[0]-1], p, dt),axis=0)
            t += dt
        return na



class Pack(Cell):
    def __init__(self):
        Cell.__init__(self,T0,v0,Pavg)
        self.S = 144  # 95 # Series
        self.P = 3  # 6 # Parallel
        self.N = self.S * self.P
        self.C = self.N * self.c
        self.E = self.N * self.e
        self.Vmax = self.S * self.vmax
        self.Vmin = self.S * self.vmin
        self.DCR = self.S / self.P * self.dcr
        self.M = self.N * self.m



def plot_var(cell, x, y1, y2):
    lbls = ['t (s)','P (W)','Voc','Impedance (Ω)','I (A)','Vcc','Ppk (W)','dE (J)','E (J)','SOE (%)','Qgen (W)','Q (J)','dT (C)','T (C)']
    clrs = ['black','gold','tab:blue','tab:pink','tab:red','tab:blue','gold','tab:green','tab:green','tab:green','tab:red','tab:red','tab:cyan','tab:cyan']
    lss = ['-','-','--','-','-','-','--',':','-','-',':','-',':','-']

    fig, ax1 = plt.subplots()
    ax1.set_xlabel(lbls[x])
    ax1.tick_params(axis='y', labelcolor='black')

    for i in y1:
        if i != 9:
            ax1.plot(cell[:,x], cell[:,i],  label=lbls[i], color=clrs[i],ls=lss[i])
        else:
            ax1.plot(cell[:, x], 100 * cell[:, i], label=lbls[i], color=clrs[i], ls=lss[i])

    ax2 = ax1.twinx()

    for i in y2:
        if i != 9:
            ax2.plot(cell[:,x], cell[:,i],  label=lbls[i], color=clrs[i],ls=lss[i])
        else:
            ax2.plot(cell[:, x], 100 * cell[:, i], label=lbls[i], color=clrs[i], ls=lss[i])

    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('')
    plt.suptitle('')
    fig.legend(loc='upper center', ncols= len(y1) + len(y2))

    fig.tight_layout()
    plt.show()



# Model
p = 48.6    # Constant power, W
T0 = 25     # Initial cell temperature, °C
v0 = 4.2    # Initial cell voltage, V
t1 = 750   # Total time elapsed, s
P28A = Cell().pwr_cycle(p, T0, v0, t1)


# Use index table to find variable indices (numbers)
# x: shared x-axis
# y1: y-variables on first axis; ex 5 & 2 are Vcc and Voc
# y2: y-variable on second axis; ex 4 & 9 are current and SOE
plot_var(P28A, 0, [5,2],[4,9])