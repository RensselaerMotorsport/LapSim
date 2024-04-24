from drivetrain_module import Drivetrain
from high_voltage_module import HighVoltage
from tire_module import Tire
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from helper_functions_ev import motor_torque
from classes.car_simple import Car
car = Car("data/rm26.json")

Vbat = 399
Ibat = 250
ωmotor = 3000

if __name__ == "__main__":
    HV = HighVoltage(Vbat, Ibat, ωmotor)
    Iin = HV.tf()
    D = Drivetrain(Iin)

    w = np.linspace(0,4500 * 60 / (2 * pi),1000)
    W = w * 2 * pi / 60
    I = np.zeros_like(w)
    T = np.zeros_like(w)
    T2 = np.zeros_like(w)
    P = np.zeros_like(w)
    for a in range(w.size):
        I[a] = HighVoltage(Vbat, Ibat, w[a]).tf()
        T[a] = Drivetrain(I[a]).tf()
        T2[a] = motor_torque(car, W[a], peak=True) * 3.5
        P[a] = I[a] * 0.94 * w[a] / 100000

    def compare_torque():

        print(D.tf())
        print(Iin * 0.94 * 42 / 12)

    def plot_current_torque_power():
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

    def plot_old_new():
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        ax1.grid()
        ax2.grid()

        ax2.set_xlabel('Motor rotational speed (RPM)')
        ax1.set_ylabel('New Wheel Torque (Nm)')
        ax2.set_ylabel('Old Wheel Torque (Nm)')

        ax1.plot(W, T)
        ax2.plot(W, T2)

        ax1.set_xlim(0, )
        ax1.set_ylim(0, )
        ax2.set_ylim(0, )
        fig.tight_layout()

        fig.show()

    def plot_tire():
        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        ax1.grid()
        ax2.grid()

        ax2.set_xlabel('Motor rotational speed (RPM)')
        ax1.set_ylabel('New Wheel Torque (Nm)')
        ax2.set_ylabel('Old Wheel Torque (Nm)')

        ax1.plot(W, T)
        ax2.plot(W, T2)

        ax1.set_xlim(0, )
        ax1.set_ylim(0, )
        ax2.set_ylim(0, )
        fig.tight_layout()

        fig.show()