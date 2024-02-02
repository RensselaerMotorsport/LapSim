
import numpy as np
# Plotly imports
import plotly.express as px
import plotly.graph_objs as go

def generate_graph(time_data, sweep_combos, value_names):
    # Convert sweep_combos to a NumPy array
    sweep_combos = np.array(sweep_combos)
    # Convert time_data to a NumPy array
    time_data = np.array(time_data)

    # Create a grid of values for the axes
    x_values = np.unique(sweep_combos[:, 0])
    y_values = np.unique(sweep_combos[:, 1])

    # Create a 2D array of time_data
    time_data_grid = time_data.reshape(len(x_values), len(y_values))

    # Create the contour plot
    contour = go.Contour(
        x=x_values,
        y=y_values,
        z=time_data_grid.T,
        colorscale=px.colors.sequential.Viridis,
        showscale=True,
        colorbar=dict(title="Time (s)"),
    )

    layout = go.Layout(
        xaxis=dict(title=value_names[0].replace('_', ' ').title()),
        yaxis=dict(title=value_names[1].replace('_', ' ').title()),
    )

    # Convert Contour object and NumPy arrays to a dictionary
    contour_dict = {
        "type": "contour",
        "x": contour.x.tolist(),  # Convert the NumPy array to a list
        "y": contour.y.tolist(),  # Convert the NumPy array to a list
        "z": contour.z.tolist(),  # Convert the NumPy array to a list
        "colorscale": contour.colorscale,
        "colorbar": {
            "title": {
                "text": contour.colorbar.title.text,
                "font": {
                    "color": "white",
                },
            },
            "tickfont": {
                "color": "white",
            },
        },
    }


    layout_dict = {
        "xaxis": {
            "title": {
                "text": layout.xaxis.title.text,
            },
            "tickfont": {
                "color": "white",
            },
            "titlefont": {
                "color": "white",
            },
            "linecolor": "white",
            "gridcolor": "white",
        },
        "yaxis": {
            "title": {
                "text": layout.yaxis.title.text,
            },
            "tickfont": {
                "color": "white",
            },
            "titlefont": {
                "color": "white",
            },
            "linecolor": "white",
            "gridcolor": "white",
        },
    }

    return [contour_dict], layout_dict  # Return a list of dictionaries and layout dictionary