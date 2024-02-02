# Basic Flask modules
from flask import (flash, make_response, redirect, render_template,
                   request, session, url_for, Blueprint)
# Local classes
from forms import rm_25_form, rm_26_form, brakes_form
from cookie_utils import can_add_cookie
from graph import generate_graph
# Looping through all possible combinations of sweep values
import itertools
# Generating range of sweep values
import numpy as np
# Additional imports
from decimal import Decimal
import importlib
import json
import os
import sys

directory = os.getcwd()
sys.path.insert(1, directory+'\\src')
sys.path.insert(1, directory+'\\src\\brakes')
from classes.car_simple import Car

output_bp = Blueprint('output_bp', __name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

#TODO: used for rm25 and it is not in use
def fill_blank_with_default(i, car):
        if request.form[i] != '':
            # gear_ratios are stored as a list in the json file, we need a special case to split it by commas
            if i == 'gear_ratios':
                car[i] = request.form[i].replace(' ','').split(',')
                # Removing any blank values (in case multiple commas in a row: 1, 2, 3,,,, 4)
                # Goes backwards through list, so we don't get index out of range
                for j in range(len(car[i])-1,-1,-1):
                    if car[i][j] == '':
                        car[i].remove('')
                    else:
                        car[i][j] = Decimal(car[i][j])
            else:
                # Otherwise, we can just convert to decimal
                car[i] = Decimal(request.form[i])

def create_form(form_name, module, operation, json_file):
    # pass in json, form name, and function and it creates a form
    # TODO: Currently the best way to do this as forms is not updated to support dynamic forms
    if json_file == 'rm25.json':
        form = rm_25_form(form_name)
    elif json_file == 'rm26.json':
        form = rm_26_form(form_name)
    elif json_file == 'brakes.json':
        form = brakes_form(form_name)
    else:
        raise ValueError(f"Unsupported json_file: {json_file}")

    length = len(form.fields)  # Get length of fields dictionary
    formatted_title = form_name.replace('_', ' ').replace('/', '').title()

    # Submit Form
    if form.is_submitted():
        # Begins with default JSON data
        car = form.data

        # Create list excluding csrf token, submit button, and also begin, step, and end values
        keys_to_exclude = ['_begin', '_end', '_step']  # Define the suffixes to exclude
        filtered_keys = []  # Create an empty list to store the filtered keys
        sweep_keys = []

        for key in list(request.form.keys())[2:]:
            if not any(key.endswith(suffix) for suffix in keys_to_exclude):
                filtered_keys.append(key)
            else:
                sweep_keys.append(key)

        values = {}
        sweep_toggled = False

        # Check Sweep and error check
        for key in sweep_keys:
            if request.form[key]:
                # Remove the suffix ('_begin', '_end', or '_step') to get the base key
                suffixes = ('_begin', '_end', '_step')
                base_key = key
                for suffix in suffixes:
                    if base_key.endswith(suffix):
                        base_key = base_key[:-len(suffix)]
                        break

                # Count the number of filled fields (begin, step, and end) for the current base_key
                filled_fields = sum(1 for suffix in ('_begin', '_step', '_end') if request.form[base_key + suffix])

                # If not all three fields (begin, step, and end) are filled, show a flash message and render the form again
                if filled_fields < 3:
                    flash(f"{base_key.replace('_', ' ').title()} sweep form isn't filled out completely.", 'success')
                    return render_template('form.html', title=formatted_title, form=form, length=length)

                # If the current key ends with '_begin', set sweep_toggled to True and store the begin, step, and end values
                if key.endswith('_begin'):
                    sweep_toggled = True
                    values[base_key] = (Decimal(request.form[base_key + '_begin']),
                                        Decimal(request.form[base_key + '_step']),
                                        Decimal(request.form[base_key + '_end']))



        if sweep_toggled:
            # Generate list of all possible combinations of sweep values
            sweep_values = []
            for key in values:
                start = Decimal(values[key][0])
                stop = Decimal(values[key][2])
                step = Decimal(values[key][1])

                decimal_array = np.arange(start, stop + step, step)
                sweep_values.append([float(d) for d in decimal_array])

            sweep_combos = list(itertools.product(*sweep_values))

            values_str = json.dumps(values, cls=DecimalEncoder)
            sweep_combos_str = json.dumps(sweep_combos, cls=DecimalEncoder)
            session['sweep_combos_str'] = sweep_combos_str
            session['values_str'] = values_str

            resp = make_response(redirect(url_for('output_bp.output', module=module, operation=operation, sweep_toggled=sweep_toggled)))

            # Loop through all possible combinations of sweep values
            for combo in sweep_combos:
                index = 0
                for i in range(len(filtered_keys)):
                    if filtered_keys[i] in values:
                        car[filtered_keys[i]] = combo[index]
                        index += 1
                    else:
                        if request.form[filtered_keys[i]] != '':
                            car[filtered_keys[i]] = Decimal(request.form[filtered_keys[i]])

                json_str = json.dumps(car, cls=DecimalEncoder, indent=2)

                new_cookie_key = f"data{combo}"
                if not can_add_cookie(session, new_cookie_key, json_str):
                    flash("Data limit exceeded. Please reduce the amount of data.")
                    return render_template('form.html', title=formatted_title, form=form, length=length)

                session[new_cookie_key] = json_str

        else:
            for i in filtered_keys:
                if request.form[i] != '':
                    car[i] = Decimal(request.form[i])

            json_obj = json.dumps(car, cls=DecimalEncoder, indent=2)
            resp = make_response(redirect(url_for('output_bp.output', module=module, operation=operation)))
            session['data'] = json_obj

        return resp

    return render_template('form.html', title=formatted_title, form=form, length=length)

@output_bp.route('/output', methods=['GET', 'POST'])
def output():
    # Retrieve args
    sweep_toggled = request.args.get('sweep_toggled')
    # Might be a security risk
    module = importlib.import_module(request.args.get('module'))
    operation = getattr(module, request.args.get('operation'))

    if sweep_toggled:
        # Retrieve args
        values = json.loads(session.get('values_str'))
        value_names = list(values.keys())
        sweep_combos = tuple(tuple(x) for x in json.loads(session.get('sweep_combos_str')))
        time_data = []
        brake_info = []
        caliperBrands = []
        padBrand = []
        caliperModel = []
        padModel = []

        for combo in sweep_combos:
            data = session.get('data' + str(combo))
            car = Car(data)
            if operation.__name__ == 'brake_input':
                brake_info_data, caliperBrands_np, padBrand_np, caliperModel_np, padModel_np = operation(car)
                brake_info.append(brake_info_data.tolist())
                caliperBrands = caliperBrands_np.tolist()
                padBrand = padBrand_np.tolist()
                caliperModel = caliperModel_np.tolist()
                padModel = padModel_np.tolist()
            else:
                time_data.append(Decimal(round(operation(car), 3)))

        if operation.__name__ == 'brake_input':
            response = make_response(render_template('brake_output.html', brake_info=brake_info, sweep_combos=sweep_combos,
                                         values=values, caliperBrands=caliperBrands, padBrand=padBrand, caliperModel=caliperModel,
                                         padModel=padModel))
        else:
            if len(value_names) == 2:
                isocontour_data, layout = generate_graph(time_data, sweep_combos, value_names)
                isocontour_data_json = json.dumps(isocontour_data, cls=DecimalEncoder)
                layout_json = json.dumps(layout, cls=DecimalEncoder)
            else:
                isocontour_data_json = None
                layout_json = None

            response = make_response(render_template('output.html', time_data=time_data, sweep_combos=sweep_combos,
                                                     values=values, isocontour_data=isocontour_data_json, layout=layout_json))

        for combo in sweep_combos:
            session.pop('data' + str(combo), None)
    else:
        data = session.get('data')
        car = Car(data)
        if operation.__name__ == 'brake_input':
            brake_info, caliperBrands_np, padBrand_np, caliperModel_np, padModel_np = operation(car)
            brake_info = [brake_info.tolist()]
            caliperBrands = caliperBrands_np.tolist()
            padBrand = padBrand_np.tolist()
            caliperModel = caliperModel_np.tolist()
            padModel = padModel_np.tolist()
            response = make_response(render_template('brake_output.html', brake_info=brake_info, caliperBrands=caliperBrands,
                                                     padBrand=padBrand, caliperModel=caliperModel, padModel=padModel))
        else:
            time_data = []
            time_data.append(Decimal(round(operation(car), 3)))
            response = make_response(render_template('output.html', time_data=time_data, sweep_combos=[], values={}))

        session.pop('data', None)

    return response