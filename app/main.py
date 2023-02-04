from flask import Flask, render_template, request #basic flask modules
from forms import straightLineForm25#, straightLineForm26 #classes from forms.py
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = '5993b6512522aa93a5306dd25249a174'

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

#straight line simulation page
@app.route('/rm25_straight_line_sim', methods=['GET', 'POST'])
def rm25_straight_line_sim():

    form = straightLineForm25('/rm25_straight_line_sim')

    # Submit Form
    if form.is_submitted():

        #writing data to a dictionary
        data_out = dict()
        data_out['mass_car'] = request.form['mass_car'] # Taking in data
        data_out['mass_driver'] = request.form['mass_driver']
        data_out['proportion_front'] = request.form['proportion_front']
        data_out['front_track_width'] = request.form['front_track_width']
        data_out['rear_track_width'] = request.form['rear_track_width']
        data_out['wheelbase'] = request.form['wheelbase']
        data_out['CG_height'] = request.form['CG_height']
        data_out['yaw_inertia'] = request.form['yaw_inertia']
        data_out['CoF'] = request.form['CoF']
        data_out['load_sensitivity'] = request.form['load_sensitivity']
        data_out['Cd'] = request.form['Cd']
        data_out['Cl'] = request.form['Cl']
        data_out['A'] = request.form['A']
        data_out['rho'] = request.form['rho']
        data_out['front_downforce'] = request.form['front_downforce']
        data_out['cp_height'] = request.form['cp_height']
        data_out['brake_bias'] = request.form['brake_bias']
        data_out['primary_drive'] = request.form['primary_drive']
        data_out['engine_sprocket_teeth'] = request.form['engine_sprocket_teeth']
        data_out['diff_sprocket_teeth'] = request.form['diff_sprocket_teeth']
        data_out['tire_radius'] = request.form['tire_radius']
        data_out['gear_ratios'] = request.form['gear_ratios']

        #formatting data
        for i in data_out.keys():
            #input dictionary and form dictionary should have same keys, so we can use i as an index for both
            #starts by replacing empty values with the default values
            if data_out[i] == '':
                data_out[i] = straightLineForm25.rm25_data[i]
            #gear ratios requires special formatting due to it being a list
            elif i == 'gear_ratios':
                data_out['gear_ratios'] = data_out['gear_ratios'].replace(' ','').split(',')
                for j in range(len(data_out['gear_ratios'])):
                    data_out['gear_ratios'][j] = float(data_out['gear_ratios'][j])
            #lastly, if the user does provide a value, just convert it to a float
            else:
                data_out[i] = float(straightLineForm25.rm25_data[i])

        #writing the dictionary to a json file (simulation program takes a json input)
        json_obj = json.dumps(data_out, indent=4)
        with open('data.json', 'w') as outfile:
            outfile.write(json_obj)
        
        return render_template('output.html') # Redirect to a different page if needed

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

if __name__ == "__main__":
    app.run(debug=False)