import math
pi = math.pi

import pandas as pd
from shapely.geometry import Polygon, Point


def get_efficiency_level(speed, torque, csv_file_path='src/data/wpd_datasets.csv'):
    # Load CSV file
    df = pd.read_csv(csv_file_path, skiprows=2, header=None)

    # Initialize data points dictionary array
    data_points = {
        str(".88"): [],
        str(".92"): [],
        str(".94"): [],
        str(".95"): [],
        str(".96"): []
    }

    # Iterate through columns in pairs (2 columns corresponds to one efficiency level).
    for i in range(0, df.shape[1], 2):
        # Assign pairs of columns to correct efficiency level based on headers in csv file
        if i == 0:
            key = str(".88")
        elif i == 2:
            key = str(".92")
        elif i == 4:
            key = str(".94")
        elif i == 6:
            key = str(".95")
        elif i == 8:
            key = str(".96")
        else:
            continue

        # for each pair of columns corresponding to efficiency level, iterate through rows
        for j in range(df.shape[0]):
            x_val = df.iloc[j, i]
            y_val = df.iloc[j, i + 1]

            # Break when Not a number is reached after last active row
            if pd.isna(x_val) or pd.isna(y_val):
                break

            # Append the x, y coordinates to the corresponding list in the dictionary
            data_points[key].append((x_val, y_val))

    # Create polygons by connecting the data points with linear segments
    polygons = {}
    for key, points in data_points.items():
        if len(points) >= 3:
            polygons[key] = Polygon(points)

    # Create a point from given speed and torque values
    point = Point(speed, torque)

    # Define the efficiency levels in order from innermost to outermost
    efficiency_order = [str(".96"), str(".95"), str(".94"), str(".92"), str(".88")]

    # Iterate from innermost to outermost to find the highest level efficiency polygon containing the point
    for efficiency in efficiency_order:
        if efficiency in polygons and polygons[efficiency].contains(point):
            return str(efficiency)

    return str(".88")

#g = get_efficiency_level(3000,215)
#print(g)

def calc_wheel_force(car, v, pbm, Voc):
    TM = car.attrs['peak_torque']
    HVeff = car.attrs['tractive_efficiency']
    DTeff = car.attrs['drivetrain_efficiency']
    GR = car.attrs['gear_ratio']
    rT = car.attrs['tire_radius']
    Kv = car.attrs['constant_kv']
    if v == 0: v = 1E-10
    MRPM = v * GR * 60 / (2 * pi * rT)
    if MRPM >= Kv * Voc: return 0
    # FUTURE: Motor efficiency mapping

    motor_lim = TM
    rules_lim = 80000 * HVeff * 30 / (MRPM * pi)
    battery_lim = pbm * HVeff * 30 / (MRPM * pi)
    power_lim = car.attrs['power_limit'] * HVeff * 30 / (MRPM * pi)
    
    torque =  min(motor_lim, rules_lim, battery_lim, power_lim) * DTeff * GR / rT
    DTeff = get_efficiency_level(MRPM, torque)
    return float(DTeff) * torque
