# Basic Flask modules
from flask import Flask, render_template
# Local classes
from app.form_creator import create_form, output_bp
# Additional imports
import os
import sys
directory = os.getcwd()
sys.path.insert(1, directory+'/src')

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Blueprints
app.register_blueprint(output_bp)

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

#straight line simulation page
@app.route('/rm25_straight_line_sim', methods=['GET', 'POST'])
def rm25_straight_line_sim():
    return create_form('/rm25_straight_line_sim', '', '', 'rm25.json')

@app.route('/rm26_acceleration', methods=['GET', 'POST'])
def rm26_acceleration():
    return create_form('/rm26_acceleration', 'acceleration', 'run_accel', 'rm26.json')

@app.route('/rm26_skidpad', methods=['GET', 'POST'])
def rm26_skidpad():
    return create_form('/rm26_skidpad', 'skidpad', 'test_skidpad', 'rm26.json')

@app.route('/brakes', methods=['GET', 'POST'])
def brakes():
    return create_form('/brakes', 'brake_form', 'brake_input', 'brakes.json')

# TODO: Make more forms!!!!!

if __name__ == "__main__":
    app.run(debug=False)
