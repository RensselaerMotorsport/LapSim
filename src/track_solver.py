import numpy as np
import matplotlib.pyplot as plt
from tires import calc_apex_speed
from tires import calc_max_longitudinal_force
from tires import calc_max_lateral_force
from tires import calc_rolling_resistance
from aerodynamics import calc_drag_force
from drivetrain import calc_wheel_force
from hvbattery import calc_peak_power
from hvbattery import calc_Voc
from hvbattery import calc_heat_gen


def list_apexes(car, ir):
    apexes = np.array([[0,calc_apex_speed(car, ir[0])]])
    for index in range(1, ir.size - 1):
        if abs(ir[index]) > abs(ir[index - 1]) and abs(ir[index]) >= abs(ir[index + 1]):
            apexes = np.append(apexes, np.array([[int(index),calc_apex_speed(car, ir[index])]]), axis=0)
    return apexes


def calc_max_decel(car, ir, v):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']
    if ir == 0: ir = 1E-10

    Fym = calc_max_lateral_force(car, v)
    Fy = m * v **2 * ir
    Fxm = calc_max_longitudinal_force(car, v)
    if (Fy/Fym)**2 >= 1: Fx = 0
    else: Fx = Fxm * ((1 - (Fy / Fym) ** 2) ** 0.5)
    return (-Fx - calc_drag_force(car, v) - calc_rolling_resistance(car, v)) / m


def calc_max_accel(car, ir, v, pbm):
    m = car.attrs['mass_car'] + car.attrs['mass_battery'] + car.attrs['mass_driver']

    Fym = calc_max_lateral_force(car, v)
    Fy = m * v ** 2 * ir
    Fxm = calc_max_longitudinal_force(car, v)
    if (Fy/Fym)**2 >= 1: Fx = 0
    else: Fx = Fxm * ((1 - (Fy / Fym) ** 2) ** 0.5) * (1 - car.attrs['proportion_front']) # In future replace with bicycle model
    FW = calc_wheel_force(car, v, pbm)
    Feff = min(Fx, FW)
    pdraw = Feff * v
    return (Feff - calc_drag_force(car, v) - calc_rolling_resistance(car, v)) / m, pdraw


class Track:
    def __init__(self, x, ir):
        self.x = x
        self.ir = ir

    def solve(self, car):
        """
        Solution array
        0: x (m) - Track position
        1: ir (1/m) - Inverse radius
        2: v (m/s) - Forward velocity
        3: t (s) - Time elapsed
        4: p (J/s) - Power drawn
        5: E
        6: SOE
        7: Voc
        8: Pbm
        9: Q
        10: T
        """
        self.solution = np.zeros((np.shape(self.x)[0],11))
        self.solution[:, 0] = self.x
        self.solution[:, 1] = self.ir
        series = car.attrs['cells_series']
        parallel = car.attrs['cells_parallel']
        capacity = car.attrs['cell_capacity']
        Cp = car.attrs['cell_thermal_capacity']
        cell_mass = series * parallel * car.attrs['cell_mass']
        self.solution[0, 5] = series * parallel * capacity * 3600
        self.solution[0, 6] = self.solution[0, 5] / (series * parallel * capacity * 3600)
        self.solution[0, 7] = series * 4.5
        self.solution[0, 8] = calc_peak_power(car, self.solution[0, 7])
        self.solution[0, 9] = cell_mass * Cp * (273 + 35)
        self.solution[0, 10] = self.solution[0, 9] / (cell_mass * Cp) - 273

        self.apexes = list_apexes(car, self.ir)
        self.dx = self.x[1] - self.x[0]

        # Step ONE: Lower apex speeds for all corners that can't slow down fast enough for the next apex
        prev_index = None # CAN SIMPLIFY AND REMOVE PREV_INDEX = NONE
        for i in range(self.apexes[:,0].size - 1,-1,-1):
            apex_index = int(self.apexes[i,0])
            if prev_index:
                v, t, p = self.back_int(car, apex_index, prev_index, i)
                self.apexes[i, 1] = min(v[0], float(self.apexes[i, 1]))
            prev_index = apex_index

        # Step TWO: Starting from beginning, start forward integrating
        for i in range(self.apexes[:,0].size - 1):
            apex_index1 = int(self.apexes[i, 0])
            apex_index2 = int(self.apexes[i + 1, 0])
            v, t, p = self.fwd_int(car, apex_index1, apex_index2)
            if not v[len(v) - 1] <= self.apexes[i + 1, 1]:
                bv, bt, bp = self.back_int(car, apex_index1, apex_index2, i)
                for j in range(len(v)):
                    if bv[j] <= v[j]:
                        v[j:len(v)] = bv[j:len(v)]
                        t[j:len(v)] = bt[j:len(v)]
                        p[j:len(v)] = bp[j:len(v)]
                        break
            self.solution[apex_index1:apex_index2 + 1, 2] = v
            self.solution[apex_index1:apex_index2 + 1, 3] = t
            self.solution[apex_index1:apex_index2 + 1, 4] = p

            for i in range(apex_index1, apex_index2 + 1):
                self.iter_battery(car, i)
        last_apex = int(self.apexes[np.shape(self.apexes)[0] - 1,0])
        last_index = np.shape(self.solution)[0]
        v, t, p = self.fwd_int(car, last_apex, last_index - 1)
        self.solution[last_apex:last_index, 2] = v
        self.solution[last_apex:last_index, 3] = t
        self.solution[last_apex:last_index, 4] = p
        for i in range(last_apex, last_index):
            self.iter_battery(car, i)
        return self.solution

    def back_int(self, car, apex_index1, apex_index2, j):
        v = [self.apexes[j + 1,1]]
        if v[0] != 0: t = [self.dx / v[0]]
        else: t = [0]
        p = [0]
        for i in range(apex_index2, apex_index1, -1):
            v.append((v[apex_index2 - i] ** 2 - 2 * self.dx * calc_max_decel(car, self.ir[i], v[len(v)-1])) ** 0.5)
            t.append(self.dx / v[apex_index2 - i])
            p.append(0)
        return v[::-1], t, p

    def fwd_int(self, car, apex_index1, apex_index2):
        v = [self.solution[apex_index1, 2]]
        if v[0] != 0: t = [self.dx / v[0]]
        else: t = [0]
        p = [0]
        HVeff = car.attrs['tractive_efficiency']
        DTeff = car.attrs['drivetrain_efficiency']
        Voc = self.solution[apex_index1, 7]
        E = self.solution[apex_index1, 5]
        Pbm = calc_peak_power(car, Voc)

        for i in range(apex_index1, apex_index2):
            v.append((v[len(v) - 1] ** 2 + 2 * self.dx * calc_max_accel(car, self.ir[i], v[len(v) - 1], Pbm)[0]) ** 0.5)
            if v[len(v) - 1] != 0: t.append(self.dx / v[len(v) - 1])
            else: t.append(0)
            p.append(calc_max_accel(car, self.ir[i], v[len(v) - 1], Pbm)[1] / (HVeff * DTeff))
            E -= p[len(v) - 1] * t[len(v) - 1]
            Voc = calc_Voc(car, E)
            Pbm = calc_peak_power(car, Voc)
        return v, t, p

    def iter_battery(self, car, i):
        if i == 0: return
        series = car.attrs['cells_series']
        parallel = car.attrs['cells_parallel']
        capacity = car.attrs['cell_capacity']
        Cp = car.attrs['cell_thermal_capacity']
        cell_mass = series * parallel * car.attrs['cell_mass']
        self.solution[i, 5] = self.solution[i - 1, 5] - self.solution[i - 1, 4] * self.solution[i - 1, 3]
        self.solution[i, 6] = self.solution[i, 5] / (series * parallel * capacity * 3600)
        self.solution[i, 7] = calc_Voc(car, self.solution[i, 5])
        self.solution[i, 8] = calc_peak_power(car, self.solution[i, 7])
        self.solution[i, 9] = self.solution[i - 1, 9] + calc_heat_gen(car, self.solution[i - 1, 7], self.solution[i - 1, 4]) * self.solution[i - 1, 3]
        self.solution[i, 10] = self.solution[i, 9] / (cell_mass * Cp) - 273

    def draw(self):
        with np.errstate(divide='ignore', invalid='ignore'):
            r = 1.0 / self.ir
        r = np.where(np.isfinite(r), r, 1E9)
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'box')
        ax.axis('off')

        # Starting point
        x, y = 0, 0
        angle = 0  # Initial direction is to the right

        # Initialize lists to store the track points
        track_x = [x]
        track_y = [y]

        for radius in r:
            # Determine the corner arc
            arc_length = 0.1
            theta = arc_length / radius  # Angle of the corner in radians

            # Calculate the corner arc points
            arc = np.linspace(0, theta, num=50)
            arc_x = radius * np.sin(arc)
            arc_y = radius * (1 - np.cos(arc))

            # Rotate the arc to match the current direction
            rotation_matrix = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]
            ])

            rotated_arc = np.dot(rotation_matrix, np.array([arc_x, arc_y]))
            track_x.extend(rotated_arc[0] + x)
            track_y.extend(rotated_arc[1] + y)

            # Update the current position and angle
            x += rotated_arc[0][-1]
            y += rotated_arc[1][-1]
            angle += theta

            # Plot the arc
            ax.plot(track_x[-50:], track_y[-50:], color='b')
        plt.tight_layout()

        plt.show()
