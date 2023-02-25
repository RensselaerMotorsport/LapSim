import matplotlib.pyplot as plt
from classes.car_simple import Car
car = Car("data/rm26.json")

def plot_tractive_force(car, maxv=100/3.6, step=0.01):
    from check_slip import calc_friction_force
    v = step
    ax = step
    F = []
    V = []
    while v < maxv:
        ax = calc_friction_force(2, ax, v)
        #while ax != calc_friction_force(2, ax, v):
        #    ax = calc_friction_force(2, ax, v)
        #    print(ax)
        V.append(v)
        F.append(ax * car.attrs["mass_car"])
        ax = step
        v += step

    plt.title("Tractive Force Diagram")
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Tractive Force (N)")
    plt.plot(V, F)
    plt.show()

plot_tractive_force(car)