function randomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgba(${r}, ${g}, ${b}, 1)`;
}

function generateYAxes(sweep_combos) {
    const yAxes = [];

    if (sweep_combos.length > 0) {
        const num_axes = sweep_combos[0].length;
        for (let i = 0; i < num_axes; i++) {
            yAxes.push({
                type: 'linear',
                position: i === 0 ? 'left' : 'right',
                display: true,
                id: `y${i}`,
                title: {
                    display: true,
                    text: `Y-axis ${i}`,
                },
                ticks: {
                    callback: function (value) {
                        return value;
                    },
                },
            });
        }
    }

    return yAxes;
}


document.addEventListener('DOMContentLoaded', function () {
    // Getting data from the HTML
    const time_data = timeData;
    const sweep_combos = sweepCombos;
    const values = values_data;
    const value_names = Object.keys(values);
    const chartElement = document.getElementById('sim_graph');
    let datasets = [];

    const yAxes = generateYAxes(sweep_combos);

    // Gen labels
    const labels = [];
    console.log(sweep_combos);
    console.log(labels);
    console.log(time_data);

    for (let i = 0; i < sweep_combos.length; i++) {
    const labelParts = [];

    for (let j = 0; j < sweep_combos[i].length; j++) {
        labelParts.push(`${value_names[j]}: ${sweep_combos[i][j]}`);
    }

    labels.push(labelParts.join(', '));
    }

    // Single Output
    if (sweep_combos.length == 0) {
        datasets = [{
            label: '',
            backgroundColor: randomColor(),
            borderColor: randomColor(),
            data: [{
                x: time_data[0],
                y: 0,
            }],
        }];
    }
    // Sweep Outputs
    else {
        for (let i = 0; i < sweep_combos.length; i++) {
            for (let j = 0; j < sweep_combos[i].length; j++) {
              const yAxisID = `y${j}`;
              datasets.push({
                label: labels[i],
                backgroundColor: randomColor(),
                borderColor: randomColor(),
                yAxisID: yAxisID,
                data: [{
                  x: time_data[i],
                  y: sweep_combos[i][j],
                }],
              });
            }
        }
        console.log(datasets);
    }

    new Chart(chartElement, {
        type: 'scatter',
        data: {
            datasets: datasets,
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (s)',
                    },
                },
                y: {
                    display: false,
                    position: 'left',
                    axes: yAxes, // Assign the generated y-axes to 'axes' property
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const time = context.parsed.x.toFixed(3);
                            return `Time: ${time}s`;
                        },
                    },
                },
                title: {
                    display: true,
                    text: 'Simulation Results',
                },
            },
        },
    });
});
