// Random color that contrast nicely with black
function randomColor() {
    const r = Math.floor(Math.random() * 128 + 128);
    const g = Math.floor(Math.random() * 128 + 128);
    const b = Math.floor(Math.random() * 128 + 128);
    return `rgba(${r}, ${g}, ${b}, 1)`;
}


document.addEventListener('DOMContentLoaded', function () {
    // Getting data from the HTML
    const time_data = timeData;
    const sweep_combos = sweepCombos;
    const values = values_data;
    const value_names = Object.keys(values);
    const chartElement = document.getElementById('sim_graph');

    // Check if double sweep
    if (value_names.length != 2) return null;

    // Creating datasets
    const datasets = sweep_combos.map((point, index) => {
        const label = `${time_data[index]} (${value_names[0]}: ${point[0]}, ${value_names[1]}: ${point[1]})`;
        return {
            label: label,
            data: [{
                x: point[0],
                y: point[1],
                label: label
            }],
            borderColor: randomColor(),
            borderWidth: 1,
            pointRadius: 2,
        };
    });

    new Chart(chartElement, {
        type: 'scatter',
        data: {
            datasets: datasets,
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: value_names[0],
                    },
                },
                y: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: value_names[1],
                    },
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        title: function (context) {
                            return context[0].dataset.label;
                        },
                        label: function (context) {
                            const xValue = context.parsed.x.toFixed(3);
                            const yValue = context.parsed.y.toFixed(3);
                            const time = context.raw.label.split(' ')[0];
                            return `Time: ${time}, ${value_names[0]}: ${xValue}, ${value_names[1]}: ${yValue}`;
                        },
                    },
                },
            },
        },
    });
});
