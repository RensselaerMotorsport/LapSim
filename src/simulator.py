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

    def draw_plots(self, car):
        self.Endurance.draw()
        self.plot(self.Endurance.solve(car))

MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')
MIS_2019.draw_plots(car)
