from flask import Flask, render_template, request, make_response, flash, redirect, url_for #basic flask modules
from forms import rm_25_form, rm_26_form #, straightLineForm26 #classes from forms.py
import itertools #for looping through all possible combinations of sweep values
import numpy #for generating range of sweep values
import json
import os
import sys
import matplotlib

directory = os.getcwd()
sys.path.insert(1, directory+'\\src')

# from test import test_func
from acceleration import run_accel
from classes.car_simple import Car
from skidpad import test_skidpad

app = Flask(__name__)

app.config['SECRET_KEY'] = '5993b6512522aa93a5306dd25249a174'

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

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
                        car[i][j] = float(car[i][j])
            else:
                #otherwise, we can just convert to float
                car[i] = float(request.form[i])

@app.route('/output', methods=['GET', 'POST'])
def output():
    # Retrive args
    sweep_toggled = request.args.get('sweep_toggled')
    # Might be a security risk
    operation = globals()[request.args.get('operation')]

    if (sweep_toggled):
        # Retrive args
        values = json.loads(request.args.get('values_str'))
        sweep_combos = tuple(tuple(x) for x in json.loads(request.args.get('sweep_combos_str')))
        time_data = []

        for combo in sweep_combos:
            data = request.cookies.get('data' + str(combo))
            if data:
                car = Car(data)
                time_data.append(float(round(operation(car), 3)))
        return render_template('output.html', time_data=time_data, sweep_combos=sweep_combos, values=values)
    else:
        data = request.cookies.get('data')
        car = Car(data)
        time_data = []
        time_data.append(float(round(operation(car), 3)))
        # Pass an empty list for sweep_combos when sweep is not toggled
        return render_template('output.html', time_data=time_data, sweep_combos=[], values={})



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
                sweep_values.append(list(numpy.arange(float(values[key][0]), float(values[key][2])+1, float(values[key][1]))))
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
            #generate list of all possible combinations of sweep values
            sweep_values = []
            for key in values:
                sweep_values.append(list(numpy.arange(float(values[key][0]), float(values[key][2])+1, float(values[key][1]))))
            sweep_combos = list(itertools.product(*sweep_values))

            values_str = json.dumps(values)
            sweep_combos_str = json.dumps(sweep_combos)
            resp = make_response(redirect(url_for('output', operation=operation, sweep_toggled=sweep_toggled,
                                                  sweep_combos_str=sweep_combos_str, values_str=values_str)))
            #loop through all possible combinations of sweep values
            for combo in sweep_combos:
                index = 0
                for i in range(len(filtered_keys)):
                    if filtered_keys[i] in values:
                        car[filtered_keys[i]] = combo[index]
                        index += 1
                    else:
                        if request.form[filtered_keys[i]] != '':
                            car[filtered_keys[i]] = float(request.form[filtered_keys[i]])

                json_obj = json.dumps(car, indent=2)

                resp.set_cookie('data' + str(combo), json_obj)
        else:
            for i in filtered_keys:
                if request.form[i] != '':
                    car[i] = float(request.form[i])

            json_obj = json.dumps(car, indent=2)
            resp = make_response(redirect(url_for('output', operation=operation)))
            resp.set_cookie('data', json_obj)
        return resp

    return render_template('form.html', title=formatted_title, form=form, length=length)

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
