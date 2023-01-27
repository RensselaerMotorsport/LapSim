from flask import Flask, redirect, render_template, url_for
from forms import straightLineForm25#, straightLineForm26

app = Flask(__name__)

app.config['SECRET_KEY'] = '5993b6512522aa93a5306dd25249a174'

#home page
@app.route('/')
def homepage():
    return render_template('home.html')

#straight line simulation page
@app.route('/rm25_straight_line_sim')
def rm25_straight_line_sim():
    form = straightLineForm25('/rm25_straight_line_sim')
    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

if __name__ == "__main__":
    app.run(debug=False)