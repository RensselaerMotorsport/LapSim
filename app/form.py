# Standard library imports
import json  # Used for loading car data from JSON files
import os    # Used for getting the current working directory to locate JSON files

# Related third-party imports
from flask_wtf import FlaskForm  # Used for creating Flask form classes
from wtforms import StringField, DecimalField, SubmitField, RadioField  # Used for creating form fields

#each perimeter from the json file if the user wants to change them
#no data is required, a blank field should use the json data

# class rm_25_form(FlaskForm):
#     directory = os.getcwd()
#     data = json.loads(open("src/data/rm25.json").read())

#     fields = {}
#     for key, value in list(data.items()):
#         label = key.replace('_', ' ').title() + ' ({})'.format(value)
#         if key == "gear_ratios":
#             fields[key] = StringField(label=label)
#             fields[key+'_begin'] = StringField('Begin Sweep')
#             fields[key+'_end'] = StringField('End Sweep')
#             fields[key+'_step'] = StringField('Step')
#         else:
#             fields[key] = DecimalField(label=label)
#             fields[key+'_begin'] = DecimalField('Begin Sweep')
#             fields[key+'_end'] = DecimalField('End Sweep')
#             fields[key+'_step'] = DecimalField('Step')
#     locals().update(fields)
#     submit = SubmitField('Calculate')

def car_form(data):
    sweep_suffixes = ['_begin', '_end', '_step']
    sweep_labels = ['Begin Sweep', 'End Sweep', 'Step']

    # Prepare a dictionary to hold field definitions
    fields = {}

    for key, value in data.items():
        # Create the main field with a dynamic label
        label = f"{key.replace('_', ' ').title()} ({value})"
        fields[key] = DecimalField(label=label)

        # Create the sweep fields (begin, end, step)
        for suffix, label_suffix in zip(sweep_suffixes, sweep_labels):
            fields[f"{key}{suffix}"] = DecimalField(label=label_suffix)

    # Add the submit button
    fields['submit'] = SubmitField('Calculate')

    # Dynamically create the form class with the fields
    DynamicCarForm = type('DynamicCarForm', (FlaskForm,), fields)

    return DynamicCarForm()

# class brakes_form(FlaskForm):

#     directory = os.getcwd()
#     data = json.loads(open("src/data/rm26.json").read()) # FIXME: Temp data replacement

#     # create fields dynamically with label set based on data
#     fields = {}
#     for key, value in list(data.items()):
#         label = key.replace('_', ' ').title() + ' ({})'.format(value)
#         fields[key] = DecimalField(label=label)

#         # add additional fields for sweep parameters
#         fields[key+'_begin'] = DecimalField('Begin Sweep')
#         fields[key+'_end'] = DecimalField('End Sweep')
#         fields[key+'_step'] = DecimalField('Step')

#     # set fields as class attributes
#     locals().update(fields)

#     # priority = RadioField('Priority', choices=[('1', 'Cost'), ('2', 'Weight'), ('3', 'Performance')])
#     submit = SubmitField('Calculate')
