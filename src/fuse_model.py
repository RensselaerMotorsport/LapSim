import matplotlib.pyplot as plt
import numpy as np

def plot_fuse(type,i2t,d=np.array([]),imax=250):
    if d.size != 0:
        x = d[0]
        y = d[1]

    i = np.linspace(1e-5, imax, 100000)
    t = np.zeros_like(i)
    for a in range(t.size):
        t[a] = i2t / i[a] ** 2

    plt.figure(dpi=200)
    plt.grid()
    plt.plot(t, i, color='tab:blue')
    if d.size != 0: plt.scatter(x, y, color='tab:orange')
    plt.xlim(0,2.5)
    plt.ylim(0,imax)
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")
    plt.title(str(type) + " fuse curve")
    plt.tight_layout()
    plt.show()

plot_fuse("Pack",720,imax=90)
#plot_fuse("Cell",54,d=np.array([[160,266,205,221,5.56,10.2,11.86,13.97,0.776,0.784,0.774,0.76,0.066,0.07,0.061,0.06],[47.15,47.15,47.15,47.15,47.32,47.33,47.35,48.59,77.66,77.58,77.71,77.52,204.24,204.31,204.41,209.72]]))
#plot_fuse("Cell",453516.99,d=np.array([[160,266,205,221,5.56,10.2,11.86,13.97,0.776,0.784,0.774,0.76,0.066,0.07,0.061,0.06],[47.15,47.15,47.15,47.15,47.32,47.33,47.35,48.59,77.66,77.58,77.71,77.52,204.24,204.31,204.41,209.72]]))
