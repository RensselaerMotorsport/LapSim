from track_solver import Track
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



class Competition:
    def __init__(self, autox_file, endurance_file):
        resolution = 0.1 # m
        autox_df = pd.read_csv(autox_file, header=None)
        endurance_df = pd.read_csv(endurance_file, header=None)
        self.Acceleration = Track(np.linspace(0, 75, int(75/resolution) + 1), np.zeros(int(75 / resolution + 1)))
        self.Skidpad = Track(np.linspace(0, 180.4, int(180.4 / resolution) + 1), np.full(int(180.4 / resolution + 1),0.11594202))
        self.Autocross = Track(autox_df[0].to_numpy(),autox_df[1].to_numpy())
        self.Endurance = Track(endurance_df[0].to_numpy(), endurance_df[1].to_numpy())
        #self.car = car

    def solve_accel(self, car):
        return self.Acceleration.solve(car)

    def plot_power_limits(self, Pmin, Pmax, car, count=100):
        result = np.zeros([int((Pmax - Pmin) / int((Pmax - Pmin) / count)),3])
        n = 0
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('Power Limit (kW)')
        ax1.set_ylabel('Final Temperature (C)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax2 = ax1.twinx()
        ax2.set_xlabel('Power Limit (kW)')
        ax2.set_ylabel('Time elapsed (s)')
        ax2.tick_params(axis='y', labelcolor='black')
        plt.title('')
        plt.suptitle('')
        fig.tight_layout()
        plt.grid()

        for i in range(Pmin, Pmax, int((Pmax - Pmin) / count)):
            print(i)
            car.attrs["power_limit"] = i
            solution = self.Endurance.solve(car)
            t = np.sum(solution[:, 3])
            result[n,:] = np.array([i, solution[np.shape(solution)[0] - 1, 10], t])
            n += 1
        ax1.plot(result[:, 0] / 1000, result[:, 1], label='T (C)', color='tab:cyan', ls='-')
        ax2.plot(result[:, 0] / 1000, result[:, 2], label='Lap Time (s)', color='tab:blue', ls='-')
        plt.legend(ncols=2)
        plt.show()

    def optimize_gear_ratio(self, car, lower_gear=2, upper_gear=4, count=1000):
        gear = np.linspace(lower_gear, upper_gear, count)
        time = np.zeros_like(gear)
        for i in range(gear.size):
            car.attrs['gear_ratio'] = gear[i]
            time[i] = np.sum(self.Acceleration.solve(car)[:, 3])
        return gear[np.argmin(time)]

    def plot_gear_ratio_vs_time(self, car, lower_gear=1.5, upper_gear=5.5, count=20):
        # Get the gear ratios and times from the optimization function
        gear = np.linspace(lower_gear, upper_gear, count)
        accel_time = np.zeros_like(gear)
        endurance_time = np.zeros_like(gear)

        for i in range(gear.size):
            car.attrs['gear_ratio'] = gear[i]
            accel_time[i] = np.sum(self.Acceleration.solve(car)[:, 3])
            endurance_time[i] = np.sum(self.Endurance.solve(car)[:, 3])

        # Use the plotter module to create the plot
        from plotter import plot_dual_yaxis
        x = gear
        y1 = [accel_time]
        y2 = [endurance_time]
        y1_labels = ["Acceleration Time"]
        y2_labels = ["Endurance Time"]
        y1_colors = ["blue"]
        y2_colors = ["green"]
        y1_ls = ["-"]
        y2_ls = ["-"]
        
        plot_dual_yaxis(x, y1, y2,
                        x_axis='Gear Ratio',
                        y1_axis='Acceleration Time (s)',
                        y2_axis='Endurance Time (s)',
                        y1_labels=y1_labels,
                        y2_labels=y2_labels,
                        y1_colors=y1_colors,
                        y2_colors=y2_colors,
                        y1_ls=y1_ls,
                        y2_ls=y2_ls)
    
    def sweep_var(self, car, xvar, min, max, count=50):
        x = np.linspace(min, max, count)
        sols = np.empty((count,), dtype=object)
        print('Variable sweep progress: 0.0%')
        for i in range(x.size):
            car.attrs[xvar] = x[i]
            car.attrs['gear_ratio'] = self.optimize_gear_ratio(car, count=100)
            sols[i] = self.Endurance.solve(car)
            print('Variable sweep progress: ' + str(round(100 * (i + 1) / count, 1)) + '%')
        return x, sols
