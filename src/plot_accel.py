from matplotlib import pyplot as plt
from helper_functions_ev import forward_int
from classes.car_simple import Car
car = Car("data/rm26.json")

plt.title("v")
plt.plot(forward_int(car, 0,20)[0])
plt.show()