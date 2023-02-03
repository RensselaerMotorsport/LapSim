from flask import Flask, render_template, request, url_for #basic flask modules
from forms import straightLineForm25#, straightLineForm26 #classes from forms.py

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

        #retreiving data (need to do tests on what empty fields return)
        mass_car = request.form['mass_car'] # Taking in data
        mass_driver = request.form['mass_driver']
        proportion_front = request.form['proportion_front']
        front_track_width = request.form['front_track_width']
        rear_track_width = request.form['rear_track_width']
        wheelbase = request.form['wheelbase']
        CG_height = request.form['CG_height']
        yaw_inertia = request.form['yaw_inertia']
        CoF = request.form['CoF']
        load_sensitivity = request.form['load_sensitivity']
        Cd = request.form['Cd']
        Cl = request.form['Cl']
        A = request.form['A']
        rho = request.form['rho']
        front_downforce = request.form['front_downforce']
        cp_height = request.form['cp_height']
        brake_bias = request.form['brake_bias']
        primary_drive = request.form['primary_drive']
        engine_sprocket_teeth = request.form['engine_sprocket_teeth']
        diff_sprocket_teeth = request.form['diff_sprocket_teeth']
        tire_radius = request.form['tire_radius']
        gear_ratios = request.form['gear_ratios']
        
        return render_template('output.html') # Redirect to a different page if needed

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

if __name__ == "__main__":
    app.run(debug=False)