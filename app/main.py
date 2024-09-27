from flask import Flask, render_template
import os

# Local imports
from app.form_creator import create_form, output_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Blueprints
app.register_blueprint(output_bp)

if __name__ == "__main__":
    app.run(debug=False)

# Home page
@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/acceleration', methods=['GET', 'POST'])
def acceleration():
    return create_form(
        '/acceleration',
        'acceleration',
        'run_accel',
        'src/data/rm28.json'
    )

# @app.route('/rm26_skidpad', methods=['GET', 'POST'])
# def rm26_skidpad():
#     return create_form(
#         '/rm26_skidpad',
#         'skidpad',
#         'test_skidpad',
#         'rm26.json'
#     )

# @app.route('/brakes', methods=['GET', 'POST'])
# def brakes():
#     return create_form('/brakes', 'brake_form', 'brake_input', 'brakes.json')