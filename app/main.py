from flask import Flask, render_template, request, make_response, flash #basic flask modules
from forms import straightLineForm25#, straightLineForm26 #classes from forms.py
import itertools #for looping through all possible combinations of sweep values
import numpy #for generating range of sweep values
import json
import os
import sys

directory = os.getcwd()
sys.path.insert(1, directory+'\\src')

from test import test_func

app = Flask(__name__)

app.config['SECRET_KEY'] = '5993b6512522aa93a5306dd25249a174'

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

def fill_blank_with_default(i, car):
        if request.form[i] != '':
                        #because gear_ratios are stored as a list in the json file, we need a special case to split it by commas
                        if i == 'gear_ratios':
                            car[i] = request.form[i].replace(' ','').split(',')
                            #removing any blank values (in case multiple commas in a row: 1, 2, 3,,,, 4)
                            #goes backwards through list so we don't get insex out of range
                            for j in range(len(car[i])-1,-1,-1):
                                if car[i][j] == '':
                                    car[i].remove('')
                                else:
                                    car[i][j] = float(car[i][j])
                        #otherwise, we can just convert to float
                        else:
                            car[i] = float(request.form[i])

#straight line simulation page
@app.route('/rm25_straight_line_sim', methods=['GET', 'POST'])
def rm25_straight_line_sim():

    form = straightLineForm25('/rm25_straight_line_sim')

    # Submit Form
    if form.is_submitted():

        #begins with default json data
        car = straightLineForm25.rm25_data
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
                        return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)
                    values[base_key] = request.form[key], request.form[base_key+'_step'], request.form[base_key+'_end']
                    sweep_toggled = True
                elif str(key).endswith('_end'):
                    base_key = str(key)[:-4]
                    if request.form[base_key+'_begin'] == '' or  request.form[base_key+'_step'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)
                elif str(key).endswith('_step'):
                    base_key = str(key)[:-5]
                    if request.form[base_key+'_begin'] == '' or request.form[base_key+'_end'] == '':
                        flash(base_key + ' sweep fourm isn\'t filled out completly.', 'success')
                        return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

        if sweep_toggled == True:
            #generate list of all possible combinations of sweep values
            sweep_values = []
            for key in values:
                sweep_values.append(list(numpy.arange(float(values[key][0]), float(values[key][2])+1, float(values[key][1]))))
            sweep_combos = list(itertools.product(*sweep_values))

            #loop through all possible combinations of sweep values
            for combo in sweep_combos:
                #ERROR: breaks here
                for i in range(min(len(filtered_keys), len(combo))):
                    if filtered_keys[i] in values:
                        car[filtered_keys[i]] = combo[i]
                    else:
                        fill_blank_with_default(filtered_keys[i], car)
                json_obj = json.dumps(car, indent=2)
                resp = make_response(output())

                # FOR DEBUGGING
                with open('output'+str(combo)+'.json', 'w') as f:
                    f.write(json_obj)

                resp.set_cookie('data' + str(combo), json_obj)

        else:
            for i in filtered_keys:
                fill_blank_with_default(i, car)
            json_obj = json.dumps(car, indent=2)
            resp = make_response(output())
            resp.set_cookie('data', json_obj)

        return resp

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
    data = request.cookies.get('data')
    test_func(data)
    return render_template('output.html', data=data)

if __name__ == "__main__":
    app.run(debug=False)