from track_solver import Track
import plotly.graph_objects as pgo
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from classes.car_simple import Car
from plotter import plot_single_yaxis
from plotter import plot_dual_yaxis

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
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Velocity (m/s)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(x, v, label='v (m/s)', color='tab:blue', ls='-')

        plt.title("Time elapsed (s): "+ str(round(t,2)))
        plt.suptitle('')
        fig.legend(loc='upper center', ncols=2)
        fig.tight_layout()
        plt.grid()
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
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Power draw (kW)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 4] / 1000, label='P (kW)', color='gold', ls='-')
        ax1.plot(solution[:, 0], solution[:, 8] / 1000, label='Ppk (kW)', color='tab:orange', ls='--')
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
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('SOE (%)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 6] * 100, label='SOE (%)', color='tab:green', ls='-')
        ax1.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax1.set_ylim(0, 100)

        ax2 = ax1.twinx()
        ax2.set_ylabel('Capacity (kWh)')
        ax2.plot(solution[:, 0], solution[:, 5] / (3.6E6), label='Capacity (kWh)', color='tab:blue', ls='-')
        ax2.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax2.set_ylim(0, solution[0, 5] / (3.6E6))
        plt.title('')
        plt.suptitle('')
        fig.legend(loc='upper center', ncols=2)
        fig.tight_layout()
        plt.grid()
        plt.show()

        # Temperature change
        fig, ax1 = plt.subplots()
        fig.set_figwidth(6.4 * 2)
        fig.set_figheight(4.8 * 2)
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Temperature (C)')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.plot(solution[:, 0], solution[:, 10], label='T (C)', color='tab:cyan', ls='-')
        ax1.set_xlim(0, solution[np.shape(solution)[0] - 1, 0])
        ax1.set_ylim(35, 70)
        #print(solution[np.shape(solution)[0] - 1, 10])

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
        sol = self.Acceleration.solve(car)
        self.plot_velocity(sol)
        #self.plot_battery(sol)

    def plot_power_limits(self, Pmin, Pmax, count=100):
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

    def optimize_gear_ratio(self, car, lower_gear=1.5, upper_gear=5.5, count=1000):
        gear = np.linspace(lower_gear, upper_gear, count)
        time = np.zeros_like(gear)
        for i in range(gear.size):
            car.attrs['gear_ratio'] = gear[i]
            time[i] = np.sum(self.Acceleration.solve(car)[:, 3])
        return gear[np.argmin(time)]

        def plot_gear_ratio_vs_time(self, car, lower_gear=1.5, upper_gear=5.5, count=1000):
        # Shorten endurance to decrease run time
        original_endurance_track = self.Endurance
        self.Endurance = Track(self.Endurance.x[:int(len(self.Endurance.x) / 20)],self.Endurance.ir[:int(len(self.Endurance.ir) / 20)])

        # Get ratios and times from above functions
        gear = np.linspace(lower_gear, upper_gear, count)
        accel_time = np.zeros_like(gear)
        endurance_time = np.zeros_like(gear)

        for i in range(gear.size):
            car.attrs['gear_ratio'] = gear[i]
            accel_time[i] = np.sum(self.Acceleration.solve(car)[:, 3])
            endurance_time[i] = np.sum(self.Endurance.solve(car)[:, 3])

        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(gear, accel_time, label="Acceleration Time", color="blue")
        ax1.set_xlabel('Gear Ratio')
        ax1.set_ylabel('Acceleration Time (s)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(gear, endurance_time, label="Endurance Time", color="green")
        ax2.set_ylabel('Endurance Single Lap Time (s)', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        fig.tight_layout()
        plt.grid(True)
        plt.title('Gear Ratio vs. Acceleration and Endurance Time')
        fig.legend(loc='upper center', ncols=2)
        plt.show()

        # Restore the original endurance track after done
        self.Endurance = original_endurance_track

    def sweep_var(self, car, xvar, yvar, min, max, count=50):
        x = np.linspace(min, max, count)
        y = np.zeros_like(x)
        for i in range(x.size):
            print(str(round(100 * (i + 1) / count,1)) + '%')
            car.attrs[xvar] = x[i]
            #car.attrs['gear_ratio'] = self.optimize_gear_ratio(car, count=200)
            sol = self.Endurance.solve(car)
            ysol = sol[:, yvar]
            y[i] = ysol[ysol.size - 1]
            times = np.zeros_like(sol[:,3])
            dQ = np.zeros_like(sol[:,9])
            for j, a in enumerate(sol[:,3]):
                if j == 0:                  
                    times[j] = a
                else:
                    times[j] = a + np.sum(sol[:j-1,3])
                    
            for j, a in enumerate(sol[:,9]):
                if j == 0:                  
                    dQ[j] = a/sol[j,3]
                else:
                    dQ[j] = (a - sol[j-1,9])/sol[j,3]

            df = pd.DataFrame(np.array([times, dQ, sol[:,10]]).T, columns=['t(s)', 'dQ/dt(W)', 'T(C)'])
            df.to_csv('data/heat_gen/' + str(int(x[i])) + 'W_limit.csv')
        return x, y


MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')

#x, y = MIS_2019.sweep_var(car, 'power_limit', 10, 10000, 80000, count=5)
x = np.array([])
y = np.array([])
for i in range(6,11):
    car.attrs["mass_battery"] += 0.057 * 95
    car.attrs['cells_parallel'] = i
    xi, yi = MIS_2019.sweep_var(car, 'power_limit', 10, 10000, 80000, count=2)
    x = np.append(x, xi)
    y = np.append(y, yi)
print(x)
print(y)

# plot_single_yaxis(x, y, 'Cells in parallel','Laptime (s)',['6P','7P','8P','9P','10P'],['#0149fe','#00637a','#005a64','#00583d','#2e4d1a'],['-','-','-','-','-','-','-','-','-','-'])

#MIS_2019.draw_plots(car)
#MIS_2019.plot_power_limits(10000,60000,count=40)
