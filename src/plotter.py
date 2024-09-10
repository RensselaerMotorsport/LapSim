import matplotlib.pyplot as plt


def plot_single_yaxis(x, y, x_axis, y_axis, y_labels, y_colors, y_ls, save_plot=None):
    fig, ax1 = plt.subplots()
    fig.set_figwidth(6.4 * 2)
    fig.set_figheight(4.8 * 2)
    ax1.set_xlabel(x_axis)
    ax1.set_ylabel(y_axis)
    ax1.tick_params(axis='x', labelcolor='black')
    ax1.tick_params(axis='y', labelcolor='black')
    for i in range(len(y_labels)):
        ax1.plot(x, y[i], label=y_labels[i], color=y_colors[i], ls=y_ls[i])
        ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(0,)
    plt.title('')
    plt.suptitle('')
    fig.legend(loc='upper center', ncols=len(y_labels))
    fig.tight_layout()
    plt.grid()
    if save_plot:
        plt.savefig(save_plot)
    plt.show()


def plot_dual_yaxis(x, y, x_axis, y_axis, y_labels, y_colors, y_ls, save_plot=None):
    pass
