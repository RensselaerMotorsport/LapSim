from flask import Flask, render_template, request, make_response, flash, redirect, url_for, session #basic flask modules
from forms import rm_25_form, rm_26_form #, straightLineForm26 #classes from forms.py
import itertools #for looping through all possible combinations of sweep values
import numpy as np#for generating range of sweep values
import plotly.graph_objs as go
import plotly.express as px
from decimal import Decimal
import json
import os
import sys

directory = os.getcwd()
sys.path.insert(1, directory+'\\src')

# from test import test_func
from acceleration import run_accel
from classes.car_simple import Car
from skidpad import test_skidpad

app = Flask(__name__)
app.secret_key = os.urandom(24)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)

def fill_blank_with_default(i, car):
        if request.form[i] != '':
            # because gear_ratios are stored as a list in the json file, we need a special case to split it by commas
            if i == 'gear_ratios':
                car[i] = request.form[i].replace(' ','').split(',')
                #removing any blank values (in case multiple commas in a row: 1, 2, 3,,,, 4)
                #goes backwards through list so we don't get insex out of range
                for j in range(len(car[i])-1,-1,-1):
                    if car[i][j] == '':
                        car[i].remove('')
                    else:
                        car[i][j] = Decimal(car[i][j])
            else:
                #otherwise, we can just convert to decimal
                car[i] = Decimal(request.form[i])

def generate_isocontour_data(time_data, sweep_combos, value_names):
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

MAX_TOTAL_COOKIE_SIZE = 100000 # Arbutary number tht can be changed later
COOKIE_OVERHEAD = 100

def cookie_size_exceeded(session, new_cookie_key, new_cookie_value):
    total_cookie_size = sum(sys.getsizeof(k) + sys.getsizeof(v) + COOKIE_OVERHEAD for k, v in session.items())
    total_cookie_size += sys.getsizeof(new_cookie_key) + sys.getsizeof(new_cookie_value) + COOKIE_OVERHEAD
    return total_cookie_size >= MAX_TOTAL_COOKIE_SIZE

def new_session_size(session, new_cookie_key, new_cookie_value):
    total_cookie_size = sum(sys.getsizeof(k) + sys.getsizeof(v) + COOKIE_OVERHEAD for k, v in session.items())
    total_cookie_size += sys.getsizeof(new_cookie_key) + sys.getsizeof(new_cookie_value) + COOKIE_OVERHEAD
    return total_cookie_size

def can_add_cookie(session, new_cookie_key, new_cookie_value):
    new_size = new_session_size(session, new_cookie_key, new_cookie_value)
    return new_size <= MAX_TOTAL_COOKIE_SIZE



@app.route('/output', methods=['GET', 'POST'])
def output():
    # Retrieve args
    sweep_toggled = request.args.get('sweep_toggled')
    # Might be a security risk
    operation = globals()[request.args.get('operation')]

    if sweep_toggled:
        # Retrieve args
        values = json.loads(session.get('values_str'))
        value_names = list(values.keys())
        sweep_combos = tuple(tuple(x) for x in json.loads(session.get('sweep_combos_str')))
        time_data = []

        for combo in sweep_combos:
            data = session.get('data' + str(combo))
            if data:
                car = Car(data)
                time_data.append(Decimal(round(operation(car), 3)))

        if len(value_names) == 2:
            isocontour_data, layout = generate_isocontour_data(time_data, sweep_combos, value_names)
            isocontour_data_json = json.dumps(isocontour_data, cls=DecimalEncoder)
            layout_json = json.dumps(layout, cls=DecimalEncoder)
        else:
            isocontour_data_json = None
            layout_json = None

        response = make_response(render_template('output.html', time_data=time_data, sweep_combos=sweep_combos, values=values, isocontour_data=isocontour_data_json, layout=layout_json))

        for combo in sweep_combos:
            session.pop('data' + str(combo), None)
    else:
        data = session.get('data')
        car = Car(data)
        time_data = []
        time_data.append(Decimal(round(operation(car), 3)))

        response = make_response(render_template('output.html', time_data=time_data, sweep_combos=[], values={}))

        session.pop('data', None)

    return response


def create_25_form(form_name, operation):

    form = rm_25_form(form_name)
    length = len(rm_25_form.fields) # get length of fields dictionary
    formatted_title = form_name.replace('_', ' ').replace('/', '').title()

    # Submit Form
    if form.is_submitted():

        #begins with default json data
        car = rm_25_form.rm25_data
        #loops through returned form data

        #create list excluding csrf token and submit button and also begin, step, and end values
        keys_to_exclude = ['_begin', '_end', '_step']  # define the suffixes to exclude
        filtered_keys = []  # create an empty list to store the filtered keys
        sweep_keys = []

        for key in list(request.form.keys())[2:]:
            if not any(key.endswith(suffix) for suffix in keys_to_exclude):
                filtered_keys.append(key)
            else:
                sweep_keys.append(key)

        values = {}
        sweep_toggled = False

        for key in sweep_keys:
            if str(request.form[key]) != '':
                #check if begin, step, and end are all filled out
                if str(key).endswith('_begin'):
                    base_key = str(key)[:-6]
                    if request.form[base_key+'_step'] == '' or request.form[base_key+'_end'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.htmml', title=formatted_title, form=form, length=length)
                    values[base_key] = request.form[key], request.form[base_key+'_step'], request.form[base_key+'_end']
                    sweep_toggled = True
                elif str(key).endswith('_end'):
                    base_key = str(key)[:-4]
                    if request.form[base_key+'_begin'] == '' or  request.form[base_key+'_step'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.html', title=formatted_title, form=form, length=length)
                elif str(key).endswith('_step'):
                    base_key = str(key)[:-5]
                    if request.form[base_key+'_begin'] == '' or request.form[base_key+'_end'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.html', title=formatted_title, form=form, length=length)

        if sweep_toggled == True:
            #generate list of all possible combinations of sweep values
            sweep_values = []
            for key in values:
                sweep_values.append(list(np.arange(Decimal(values[key][0]), Decimal(values[key][2])+1, Decimal(values[key][1]))))
            sweep_combos = list(itertools.product(*sweep_values))

            resp = make_response(redirect('/output'))
            #loop through all possible combinations of sweep values
            for combo in sweep_combos:
                #ERROR: breaks here
                for i in range(min(len(filtered_keys), len(combo))):
                    if filtered_keys[i] in values:
                        car[filtered_keys[i]] = combo[i]
                    else:
                        fill_blank_with_default(filtered_keys[i], car)
                json_obj = json.dumps(car, indent=2)

                # FOR DEBUGGING
                # with open('output'+str(combo)+'.json', 'w') as f:
                #     f.write(json_obj)

                resp.set_cookie('data' + str(combo), json_obj)

        else:
            for i in filtered_keys:
                fill_blank_with_default(i, car)
            json_obj = json.dumps(car, indent=2)
            resp = make_response(redirect('/output'))
            resp.set_cookie('data', json_obj)
        return resp

    return render_template('form.html', title=formatted_title, form=form, length=length)

# TODO: add RM_25 support and json
# pass in json, form name, and function and it creates a form
def create_26_form(form_name, operation):
    form = rm_26_form(form_name)
    length = len(rm_26_form.fields) # get length of fields dictionary
    formatted_title = form_name.replace('_', ' ').replace('/', '').title()

    # Submit Form
    if form.is_submitted():

        #begins with default json data
        car = rm_26_form.data
        #loops through returned form data

        #create list excluding csrf token and submit button and also begin, step, and end values
        keys_to_exclude = ['_begin', '_end', '_step']  # define the suffixes to exclude
        filtered_keys = []  # create an empty list to store the filtered keys
        sweep_keys = []

        for key in list(request.form.keys())[2:]:
            if not any(key.endswith(suffix) for suffix in keys_to_exclude):
                filtered_keys.append(key)
            else:
                sweep_keys.append(key)

        values = {}
        sweep_toggled = False

        for key in sweep_keys:
            if str(request.form[key]) != '':
                #check if begin, step, and end are all filled out
                if str(key).endswith('_begin'):
                    base_key = str(key)[:-6]
                    if request.form[base_key+'_step'] == '' or request.form[base_key+'_end'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.html', title=formatted_title, form=form, length=length)
                    values[base_key] = request.form[key], request.form[base_key+'_step'], request.form[base_key+'_end']
                    sweep_toggled = True
                elif str(key).endswith('_end'):
                    base_key = str(key)[:-4]
                    if request.form[base_key+'_begin'] == '' or  request.form[base_key+'_step'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.html', title=formatted_title, form=form, length=length)
                elif str(key).endswith('_step'):
                    base_key = str(key)[:-5]
                    if request.form[base_key+'_begin'] == '' or request.form[base_key+'_end'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('form.html', title=formatted_title, form=form, length=length)

        if sweep_toggled == True:
            # generate list of all possible combinations of sweep values
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

            resp = make_response(redirect(url_for('output', operation=operation, sweep_toggled=sweep_toggled)))

            # loop through all possible combinations of sweep values
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
            resp = make_response(redirect(url_for('output', operation=operation)))
            session['data'] = json_obj
        return resp

    return render_template('form.html', title=formatted_title, form=form, length=length)

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

#straight line simulation page
@app.route('/rm25_straight_line_sim', methods=['GET', 'POST'])
def rm25_straight_line_sim():
    return create_25_form('/rm25_straight_line_sim', '')

@app.route('/rm26_acceleration', methods=['GET', 'POST'])
def rm26_acceleration():
    return create_26_form('/rm26_acceleration', 'run_accel')

@app.route('/rm26_skidpad', methods=['GET', 'POST'])
def rm26_skidpad():
    return create_26_form('/rm26_skidpad', 'test_skidpad')

#TODO: Make more forms!!!!!

if __name__ == "__main__":
    app.run(debug=False)
