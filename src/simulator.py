from track_solver import Track
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from classes.car_simple import Car
car = Car("data/rm28.json")


class Competition:
    def __init__(self, autox_file, endurance_file):
        resolution = 0.1 # m
        autox_df = pd.read_csv(autox_file, header=None)
        endurance_df = pd.read_csv(endurance_file, header=None)
        self.Acceleration = Track(np.linspace(0, 75, int(75/resolution) + 1), np.zeros(int(75 / resolution + 1)))
        self.Skidpad = Track(np.linspace(0, 180.4, int(180.4 / resolution) + 1), np.full(int(180.4 / resolution + 1),0.11594202))
        self.Autocross = Track(autox_df[0].to_numpy(),autox_df[1].to_numpy())
        self.Endurance = Track(endurance_df[0].to_numpy(), endurance_df[1].to_numpy())

    def plot_velocity(self, solution):
        x = solution[:, 0]
        v = solution[:, 2]
        t = 0
        for i in solution[:, 3]:
            t += i
        plt.plot(x,v)
        plt.title("Time elapsed (s): "+ str(round(t,2)))
        plt.show()

        #pwr = solution[:, 4]
        #plt.plot(x,pwr)
        #plt.title("Time elapsed (s): "+ str(round(t,2)))
        #plt.show()

    def plot_battery(self, solution):
        lbls = ['t (s)', 'P (W)', 'Voc', 'Impedance (Ω)', 'I (A)', 'Vcc', 'Ppk (W)', 'dE (J)', 'E (J)', 'SOE (%)',
                'Qgen (W)', 'Q (J)', 'dT (C)', 'T (C)']
        clrs = ['black', 'gold', 'tab:blue', 'tab:pink', 'tab:red', 'tab:blue', 'gold', 'tab:green', 'tab:green',
                'tab:green', 'tab:red', 'tab:red', 'tab:cyan', 'tab:cyan']
        lss = ['-', '-', '--', '-', '-', '-', '--', ':', '-', '-', ':', '-', ':', '-']
        # Power Draw
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('t (s)')
        ax1.set_ylabel('Power draw (kW)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 4] / 1000, label='P (kW)', color='gold', ls='-')
        ax1.plot(solution[:, 0], solution[:, 8] / 1000, label='Ppk (kW)', color='gold', ls='--')
        ax1.set_xlim(0,solution[np.shape(solution)[0] - 1, 0])
        ax1.set_ylim(0,80)

        plt.title('')
        plt.suptitle('')
        fig.legend(loc='upper center', ncols=2)
        fig.tight_layout()
        plt.grid()
        plt.show()

        # Capacity and Energy
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('t (s)')
        ax1.set_ylabel('SOE (%)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 6] * 100, label='SOE (%)', color='tab:green', ls='-')
        ax1.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax1.set_ylim(0, 100)

        ax2 = ax1.twinx()
        ax2.set_ylabel('Capacity (kWh)')
        ax2.plot(solution[:, 0], solution[:, 5] / (3.6E6), label='Capacity (kWh)', color='tab:blue', ls='-')
        ax2.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax2.set_ylim(0, solution[np.shape(solution)[0] - 1, 5] / (3.6E6))
        plt.title('')
        plt.suptitle('')
        fig.legend(loc='upper center', ncols=2)
        fig.tight_layout()
        plt.grid()
        plt.show()

        # Temperature change
        print(solution[:, 10])
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('t (s)')
        ax1.set_ylabel('Temperature (C)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 10], label='T (C)', color='tab:cyan', ls='-')
        ax1.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax1.set_ylim(35, 70)

        ax2 = ax1.twinx()
        ax2.set_ylabel('Heat Capacity (MJ)')
        ax2.plot(solution[:, 0], solution[:, 9] / 1E6, label='Q (MJ)', color='tab:red', ls='-')
        ax2.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        #ax2.set_ylim(0, solution[np.shape(solution)[0] - 1, 9] / 1E6)
        plt.title('')
        plt.suptitle('')
        fig.legend(loc='upper center', ncols=2)
        fig.tight_layout()
        plt.grid()
        plt.show()

    def draw_plots(self, car):
        #self.Endurance.draw()
        self.plot_battery(self.Endurance.solve(car))

MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')
MIS_2019.draw_plots(car)
