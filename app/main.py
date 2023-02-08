from flask import Flask, render_template, request, make_response #basic flask modules
from forms import straightLineForm25#, straightLineForm26 #classes from forms.py
import json
import os

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

        #begins with default json data
        car = straightLineForm25.rm25_data
        #loops through returned form data
        #we need to slice from element 2 onward because [0] is a csrf token and [1] is the submit button
        for i in list(request.form.keys())[2:]:
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

        #writing the dictionary to a json file (simulation program takes a json input)
        # directory = os.getcwd()
        json_obj = json.dumps(car, indent=2)
        # with open(directory+'\\src\\data\\data.json', 'w') as outfile:
        #     outfile.write(json_obj)

        resp = make_response(output())
        resp.set_cookie('data', json_obj)
        
        return resp
        # return render_template('output.html') # Redirect to a different page if needed

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
    data = request.cookies.get('data')
    return render_template('output.html', data=data)

if __name__ == "__main__":
    app.run(debug=False)