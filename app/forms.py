from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
import json #car data
import os #get current working directory for json file

#each perimeter from the json file if the user wants to change them
#no data is required, a blank field should use the json data

class rm_25_form(FlaskForm):
    directory = os.getcwd()
    data = json.loads(open(directory+"\\app\\rm25.json").read())

    fields = {}
    for key, value in list(data.items()):
        label = key.replace('_', ' ').title() + ' ({})'.format(value)
        if label == "gear ratios":
            fields[key] = StringField(label=label)
            fields[key+'_begin'] = StringField('Begin Sweep')
            fields[key+'_end'] = StringField('End Sweep')
            fields[key+'_step'] = StringField('Step')
        else:
            fields[key] = DecimalField(label=label)
            fields[key+'_begin'] = DecimalField('Begin Sweep')
            fields[key+'_end'] = DecimalField('End Sweep')
            fields[key+'_step'] = DecimalField('Step')
    locals().update(fields)
    submit = SubmitField('Calculate')

# TODO: We might be able to pass in the json file and have one function
class rm_26_form(FlaskForm):

    directory = os.getcwd()
    data = json.loads(open(directory+"\\app\\rm26.json").read())

    # create fields dynamically with label set based on data
    fields = {}
    for key, value in list(data.items()):
        label = key.replace('_', ' ').title() + ' ({})'.format(value)
        fields[key] = DecimalField(label=label)

        # add additional fields for sweep parameters
        fields[key+'_begin'] = DecimalField('Begin Sweep')
        fields[key+'_end'] = DecimalField('End Sweep')
        fields[key+'_step'] = DecimalField('Step')

    # set fields as class attributes
    locals().update(fields)

    submit = SubmitField('Calculate')