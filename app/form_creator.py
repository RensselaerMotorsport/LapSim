import itertools  # Looping through all possible combinations of sweep values
import decimal
import importlib
import json
import numpy as np  # Generating range of sweep values
from flask import (flash, make_response, redirect, render_template, request,
                   session, url_for, Blueprint)

# Local imports
from app.form import car_form
from app.cookie_utils import can_add_cookie
from app.graph import generate_graph
from src.classes.car_simple import Car
from src.simulator import Competition

output_bp = Blueprint('output_bp', __name__)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal):
            return str(o)
        return super().default(o)

#TODO: used for rm25 and it is not in use
# def fill_blank_with_default(i, car):
#         if request.form[i] != '':
#             # gear_ratios are stored as a list in the json file, we need a special case to split it by commas
#             if i == 'gear_ratios':
#                 car[i] = request.form[i].replace(' ','').split(',')
#                 # Removing any blank values (in case multiple commas in a row: 1, 2, 3,,,, 4)
#                 # Goes backwards through list, so we don't get index out of range
#                 for j in range(len(car[i])-1,-1,-1):
#                     if car[i][j] == '':
#                         car[i].remove('')
#                     else:
#                         car[i][j] = decimal(car[i][j])
#             else:
#                 # Otherwise, we can just convert to decimal
#                 car[i] = decimal(request.form[i])

def create_form(form_name, module, operation, json_file):
    # Load data from JSON file
    with open(json_file) as f:
        data = json.load(f)

    form = car_form(data)
    formatted_title = form_name.replace('_', ' ').replace('/', '').title()

    # Check if the form is submitted
    if form.is_submitted():
        car = form.data

        filtered_keys, sweep_keys = get_filtered_and_sweep_keys(request.form)

        # values, sweep_toggled = process_sweep_keys(sweep_keys, request.form, form, formatted_title)

        # Handle sweep cases
        if False: #sweep_toggled: # FIXME: Temp disable sweep so can debug
            return handle_sweep(filtered_keys, values, car, module, operation)
        else:
            return handle_regular_submission(filtered_keys, car, form, formatted_title, module, operation)

    # Render the form if not submitted
    return render_template('form.html', title=formatted_title, form=form, length=len(form._fields))

def get_filtered_and_sweep_keys(form_data):
    """Filter out keys that are sweep-related and return filtered and sweep keys."""
    keys_to_exclude = ['_begin', '_end', '_step']
    filtered_keys = [key for key in list(form_data.keys())[2:] if not any(key.endswith(suffix) for suffix in keys_to_exclude)]
    sweep_keys = [key for key in list(form_data.keys())[2:] if any(key.endswith(suffix) for suffix in keys_to_exclude)]
    return filtered_keys, sweep_keys

def process_sweep_keys(sweep_keys, form_data, form, title):
    """Process sweep keys and validate that all sweep-related fields are filled."""
    values = {}
    sweep_toggled = False

    for key in sweep_keys:
        if form_data[key]:
            base_key = get_base_key(key)

            if not are_sweep_fields_filled(base_key, form_data):
                flash(f"{base_key.replace('_', ' ').title()} sweep form isn't filled out completely.", 'error')
                return values, sweep_toggled

            if key.endswith('_begin'):
                sweep_toggled = True
                values[base_key] = (
                    decimal(form_data[base_key + '_begin']),
                    decimal(form_data[base_key + '_step']),
                    decimal(form_data[base_key + '_end'])
                )

    return values, sweep_toggled

def get_base_key(key):
    """Extract base key by removing sweep suffixes."""
    for suffix in ['_begin', '_end', '_step']:
        if key.endswith(suffix):
            return key[:-len(suffix)]
    return key

def are_sweep_fields_filled(base_key, form_data):
    """Check if all sweep fields (begin, step, end) are filled for a given base key."""
    return all(form_data.get(f"{base_key}{suffix}") for suffix in ['_begin', '_step', '_end'])

def handle_sweep(filtered_keys, values, car, module, operation):
    """Handle the sweep logic by creating combinations of sweep values."""
    sweep_values = [
        list(np.arange(decimal(values[key][0]), Decimal(values[key][2]) + Decimal(values[key][1]), Decimal(values[key][1])))
        for key in values
    ]

    sweep_combos = list(itertools.product(*sweep_values))
    save_sweep_data_to_session(values, sweep_combos)

    for combo in sweep_combos:
        update_car_data(filtered_keys, values, car, combo)
        json_str = json.dumps(car, cls=DecimalEncoder, indent=2)

        if not can_add_cookie(session, f"data{combo}", json_str):
            flash("Data limit exceeded. Please reduce the amount of data.")
            return render_template('form.html', title="Error", form=form)

        session[f"data{combo}"] = json_str

    return make_response(redirect(url_for('output_bp.output', module=module, operation=operation, sweep_toggled=True)))

def handle_regular_submission(filtered_keys, car, form, title, module, operation):
    """Handle a regular (non-sweep) form submission."""
    for key in filtered_keys:
        if request.form[key]:
            car[key] = decimal(request.form[key])

    json_obj = json.dumps(car, cls=DecimalEncoder, indent=2)
    session['data'] = json_obj

    return make_response(redirect(url_for('output_bp.output', module=module, operation=operation)))

def save_sweep_data_to_session(values, sweep_combos):
    """Save sweep data and combinations to the session."""
    session['sweep_combos_str'] = json.dumps(sweep_combos, cls=DecimalEncoder)
    session['values_str'] = json.dumps(values, cls=DecimalEncoder)

def update_car_data(filtered_keys, values, car, combo):
    """Update car data with a combination of sweep values."""
    index = 0
    for i in range(len(filtered_keys)):
        if filtered_keys[i] in values:
            car[filtered_keys[i]] = combo[index]
            index += 1
        elif request.form[filtered_keys[i]]:
            car[filtered_keys[i]] = decimal(request.form[filtered_keys[i]])

# move this to output.py
@output_bp.route('/output', methods=['GET', 'POST'])
def output():
    # Retrieve args
    sweep_toggled = request.args.get('sweep_toggled')
    # Might be a security risk
    # module = importlib.import_module(request.args.get('module'))
    operation = request.args.get('operation')

    comp = Competition(
        'src/data/2018MichiganAXTrack_new.csv',
        'src/data/2019MichiganEnduranceTrack.csv'
    )

    operation_method = getattr(comp, operation)

    if False: #sweep_toggled: # FIXME: Temp disable sweep so can debug
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
                time_data.append(decimal(round(operation(car), 3)))

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
        car = Car("src/data/rm28.json") # FIXME should be a dynamic file

        # if operation.__name__ == 'brake_input':
        #     brake_info, caliperBrands_np, padBrand_np, caliperModel_np, padModel_np = operation(car)
        #     brake_info = [brake_info.tolist()]
        #     caliperBrands = caliperBrands_np.tolist()
        #     padBrand = padBrand_np.tolist()
        #     caliperModel = caliperModel_np.tolist()
        #     padModel = padModel_np.tolist()
        #     response = make_response(render_template('brake_output.html', brake_info=brake_info, caliperBrands=caliperBrands,
        #                                              padBrand=padBrand, caliperModel=caliperModel, padModel=padModel))
        # else:
        time_data = []
        # print(operation_method.solve(car)[3])
        time_data.extend(operation_method.solve(car)[3])
        response = make_response(render_template('output.html', time_data=time_data, sweep_combos=[], values={}))

        session.pop('data', None)

    return response
