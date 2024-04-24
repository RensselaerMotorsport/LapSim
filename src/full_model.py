from drivetrain_module import Drivetrain
from high_voltage_module import HighVoltage
import numpy as np
import matplotlib.pyplot as plt
from math import pi

Vbat = 399
Ibat = 250
ωmotor = 3000

if __name__ == "__main__":
    HV = HighVoltage(Vbat, Ibat, ωmotor)
    Iin = HV.tf()
    D = Drivetrain(Iin)
    print(D.tf())
    print(Iin * 0.94 * 42 / 12)

    w = np.linspace(0,4500 * 60 / (2 * pi),1000)
    W = w * 2 * pi / 60
    I = np.zeros_like(w)
    T = np.zeros_like(w)
    P = np.zeros_like(w)
    for a in range(w.size):
        I[a] = HighVoltage(Vbat, Ibat, w[a]).tf()
        T[a] = Drivetrain(I[a]).tf()
        P[a] = I[a] * 0.94 * w[a] / 100000

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

    ax1.grid()
    ax2.grid()
    ax3.grid()

    ax3.set_xlabel('Motor rotational speed (RPM)')
    ax1.set_ylabel('Current (A)')
    ax2.set_ylabel('Wheel Torque (Nm)')
    ax3.set_ylabel('Power (kW)')
    #fig.suptitle("EMRAX 228 HV")

    ax1.plot(W,I)
    ax2.plot(W,T)
    ax3.plot(W, P)

    ax1.set_xlim(0,)
    ax1.set_ylim(0,)
    ax2.set_ylim(0,)
    ax3.set_ylim(0, )
    fig.tight_layout()

    fig.show()