from flask import Flask, render_template, request #basic flask modules
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

        #writing data to a dictionary
        car = dict()
        #we need to slice out the first 2 values of the form data since those are a secret key, and the submit button
        #hence list(request.form.keys())[2:]
        for i in list(request.form.keys())[2:]:
            car[i] = request.form[i]

        #formatting data
        for i in car.keys():
            #input dictionary and form dictionary should have same keys, so we can use i as an index for both
            #starts by replacing empty values with the default values
            if car[i] == '':
                car[i] = straightLineForm25.rm25_data[i]
            #gear ratios requires special formatting due to it being a list
            elif i == 'gear_ratios':
                car['gear_ratios'] = car['gear_ratios'].replace(' ','').split(',')
                for j in range(len(car['gear_ratios'])):
                    car['gear_ratios'][j] = float(car['gear_ratios'][j])
            #lastly, if the user does provide a value, just convert it to a float
            else:
                car[i] = float(car[i])

        #writing the dictionary to a json file (simulation program takes a json input)
        directory = os.getcwd()
        json_obj = json.dumps(car, indent=2)
        with open(directory+'\\src\\data\\data.json', 'w') as outfile:
            outfile.write(json_obj)
        
        return render_template('output.html') # Redirect to a different page if needed

    return render_template('rm25_straight_line_sim.html', title="RM25 Staight Line Sim", form=form)

if __name__ == "__main__":
    app.run(debug=False)