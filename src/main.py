from classes.car_simple import Car
from simulator import Competition
import numpy as np
import matplotlib.pyplot as plt

car = Car("data/rm28.json")
MIS_2019 = Competition('data/2018MichiganAXTrack_new.csv', 'data/2019MichiganEnduranceTrack.csv')


def sweep_parallel_count():
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


def plot_velocity(solution):
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


def plot_battery(solution):
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


if __name__ == '__main__':
    '''Outputs heat gen csvs'''
    print('yo')