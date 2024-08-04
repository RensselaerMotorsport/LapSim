from hvbattery import Cell
import matplotlib.pyplot as plt
import pandas as pd


def plot_var(cell, x, y1, y2):
    lbls = ['t (s)','P (W)','Voc','Impedance (Ω)','I (A)','Vcc','Ppk (W)','dE (J)','E (J)','SOE (%)','Qgen (W)','Q (J)','dT (C)','T (C)']
    clrs = ['black','gold','tab:blue','tab:pink','tab:red','tab:blue','gold','tab:green','tab:green','tab:green','tab:red','tab:red','tab:cyan','tab:cyan']
    lss = ['-','-','--','-','-','-','--',':','-','-',':','-',':','-']

    fig, ax1 = plt.subplots()
    ax1.set_xlabel(lbls[x])
    ax1.tick_params(axis='y', labelcolor='black')

    for i in y1:
        if i != 9:
            ax1.plot(cell[:,x], cell[:,i],  label=lbls[i], color=clrs[i],ls=lss[i])
        else:
            ax1.plot(cell[:, x], 100 * cell[:, i], label=lbls[i], color=clrs[i], ls=lss[i])

    ax2 = ax1.twinx()

    for i in y2:
        if i != 9:
            ax2.plot(cell[:,x], cell[:,i],  label=lbls[i], color=clrs[i],ls=lss[i])
        else:
            ax2.plot(cell[:, x], 100 * cell[:, i], label=lbls[i], color=clrs[i], ls=lss[i])

    ax2.tick_params(axis='y', labelcolor='black')

    plt.title('')
    plt.suptitle('')
    fig.legend(loc='upper center', ncols= len(y1) + len(y2))

    fig.tight_layout()
    plt.show()



# Model
#p = 48.6    # Constant power, W
T0 = 25     # Initial cell temperature, °C
v0 = 4.2    # Initial cell voltage, V
t1 = 750   # Total time elapsed, s


df = pd.read_excel('Book1.xlsx')
t = df["Time step (s)"]
t = t.to_numpy()
p = df["Power per cell (W)"]
p = p.to_numpy()

P28A = Cell().pwr_cycle(p, T0, v0, t)

cell_df = pd.DataFrame(P28A, columns = ['t (s)','P (W)','Voc','Impedance (Ω)','I (A)','Vcc','Ppk (W)','dE (J)','E (J)','SOE (%)','Qgen (W)','Q (J)','dT (C)','T (C)'])
with pd.ExcelWriter("Cell output data.xlsx") as writer:
    cell_df.to_excel(writer, index=False)

# Use index table to find variable indices (numbers)
# x: shared x-axis
# y1: y-variables on first axis; ex 5 & 2 are Vcc and Voc
# y2: y-variable on second axis; ex 4 & 9 are current and SOE
#plot_var(P28A, 0, [5,2],[4,9])
plot_var(P28A, 0, [5,2],[9])
plot_var(P28A, 0, [1,6,10],[])
plot_var(P28A, 0, [9],[])
plot_var(P28A, 0, [13],[])
