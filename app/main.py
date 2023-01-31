from flask import Flask, redirect, render_template, url_for #basic flask modules
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
        mass_car = form.mass_car.data # Taking in data
        mass_driver = form.mass_driver.data
        proportion_front = form.proportion_front.data
        front_track_width = form.front_track_width.data
        rear_track_width = form.rear_track_width.data
        wheelbase = form.wheelbase.data
        CG_height = form.CG_height.data
        yaw_inertia = form.yaw_inertia.data
        CoF = form.CoF.data
        load_sensitivity = form.load_sensitivity.data
        Cd = form.Cd.data
        Cl = form.Cl.data
        A = form.A.data
        rho = form.rho.data
        front_downforce = form.front_downforce.data
        cp_height = form.cp_height.data
        brake_bias = form.brake_bias.data
        primary_drive = form.primary_drive.data
        engine_sprocket_teeth = form.engine_sprocket_teeth.data
        diff_sprocket_teeth = form.diff_sprocket_teeth.data
        tire_radius = form.tire_radius.data
        gear_ratios = form.gear_ratios.data

        return render_template('output.html') # Redirect to a different page if needed

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

if __name__ == "__main__":
    app.run(debug=False)