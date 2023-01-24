from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('basic.html')

@app.route("/InputForm")
def input_form():
    return render_template('inputform.html')