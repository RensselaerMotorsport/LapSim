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
    const curves = curves_data;
    console.log("time_data: ", time_data);
    console.log("sweep_combos: ", sweep_combos);
    console.log("values: ", values);
    console.log("value_names: ", value_names);
    console.log("curves: ", curves);

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

    // Creating curve datasets
    function curveDatasets(curves) {
        console.log("curves: ", curves);
        return curves.map((curve, index) => {
            console.log("curve: ", curve);
            console.log("index: ", index);
            if (curve === null) return null; // Skip if curve is null

            const label = `Curve for ${time_data[index]}s`;
            console.log("label: ", label);
            return {
                label: label,
                data: curve.map((point) => ({
                    x: point[0],
                    y: point[1]
                })),
                borderColor: randomColor(),
                borderWidth: 1,
                pointRadius: 0,
                tension: 0.4,
                fill: false,
            };
        }).filter(dataset => dataset !== null); // Remove null datasets from the array
    }

    console.log("datasets: ", datasets);
    console.log("curveDatasets(curves): ", curveDatasets(curves));

    // Create the chart
    new Chart(chartElement, {
        type: 'scatter',
        data: {
            datasets: [...datasets, ...curveDatasets(curves)],
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
