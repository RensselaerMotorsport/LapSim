import matplotlib.pyplot as plt


def plot_single_yaxis(x, y, x_axis, y_axis, y_labels, y_colors, y_ls, y_lim=None, save_plot=None, vline=None, vline_style=None):
    import matplotlib.pyplot as plt

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

    if y_lim:
        ax1.set_ylim(y_lim)
    else:
        ax1.set_ylim(0, )

    if vline is not None:
        ax1.axvline(x=vline, **(vline_style or {'color': 'black', 'linestyle': '--'}))

    plt.title('')
    plt.suptitle('')
    fig.legend(loc='upper center', ncols=len(y_labels))
    fig.tight_layout()
    plt.grid()

    if save_plot:
        plt.savefig(save_plot)
    plt.show()


def plot_dual_yaxis(x, y1, y2, x_axis, y1_axis, y2_axis, y1_labels, y2_labels, y1_colors, y2_colors, y1_ls, y2_ls, save_plot=None):
    fig, ax1 = plt.subplots()
    fig.set_figwidth(6.4 * 2)
    fig.set_figheight(4.8 * 2)

    # First Y-axis
    ax1.set_xlabel(x_axis)
    ax1.set_ylabel(y1_axis)
    ax1.tick_params(axis='x', labelcolor='black')
    ax1.tick_params(axis='y', labelcolor='black')

    for i in range(len(y1_labels)):
        ax1.plot(x, y1[i], label=y1_labels[i], color=y1_colors[i], ls=y1_ls[i])
    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(0,)

    # Second Y-axis
    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_axis)

    for i in range(len(y2_labels)):
        ax2.plot(x, y2[i], label=y2_labels[i], color=y2_colors[i], ls=y2_ls[i])
    ax2.set_ylim(0,)

    #Legends
    lines_labels_1 = [ax1.get_lines()[i] for i in range(len(y1_labels))]
    lines_labels_2 = [ax2.get_lines()[i] for i in range(len(y2_labels))]
    ax1.legend(lines_labels_1 + lines_labels_2, y1_labels + y2_labels, loc='upper center', ncols=len(y1_labels) + len(y2_labels))
    if save_plot:
        plt.savefig(save_plot)
    plt.tight_layout()
    plt.grid()
    plt.show()

