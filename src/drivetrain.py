import math
pi = math.pi
import pandas as pd

# Dictionary to store the efficiency data after loading the CSV
efficiency_data = {
    ".88": [],
    ".92": [],
    ".94": [],
    ".95": [],
    ".96": []
}

def is_point_in_polygon(x, y, polygon):
    # Determines if point is within a polygon
    num_points = len(polygon)
    inside = False

    x0, y0 = polygon[0]

    for i in range(1, num_points + 1):
        x1, y1 = polygon[i % num_points]

        if y > min(y0, y1):
            if y <= max(y0, y1):
                if x <= max(x0, x1):
                    if y0 != y1:
                        x_intersection = (y - y0) * (x1 - x0) / (y1 - y0) + x0
                    if x0 == x1 or x <= x_intersection:
                        inside = not inside

        x0, y0 = x1, y1

    return inside

def load_efficiency_data(csv_file_path='data/wpd_datasets.csv'):
    # Load CSV file only once and store data in global dictionary
    global efficiency_data
    df = pd.read_csv(csv_file_path, skiprows=2, header=None)

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
            efficiency_data[key].append((x_val, y_val))

def get_efficiency_level(speed, torque):
    # Define the efficiency levels in order from innermost to outermost
    efficiency_order = [".96", ".95", ".94", ".92", ".88"]

    # Iterate from innermost to outermost to find the highest level efficiency polygon containing the point
    for efficiency in efficiency_order:
        polygon = efficiency_data[efficiency]
        if len(polygon) >= 3 and is_point_in_polygon(speed, torque, polygon):
            return efficiency

    # Default to .88 if no match found
    return ".88"

load_efficiency_data('data/wpd_datasets.csv')

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
    
    torque =  min(motor_lim, rules_lim, battery_lim, power_lim) * GR / rT
    DTeff = get_efficiency_level(MRPM, torque)
    return float(DTeff) * torque
