from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import json #car data
import os #get current working directory for json file

#CHANGE THIS TO PROPER DIRECTORY BEFORE DEPLOYMENT
#rm26_data = json.loads(open('C:\\Users\\fornem\\Dropbox\\lapsim\\lapsim_final\\rm26.json').read())

#each perimeter from the json file if the user wants to change them
#no data is required, a blank field should use the json data
#the data returned from these forms will be plugged into the helper functions (need to figure out how to incorporate those)
#helper functions and straight line sim program are found in src branch of repo
class straightLineForm25(FlaskForm):

    directory = os.getcwd()
    rm25_data = json.loads(open(directory+"\\rm25.json").read())

    #each field for data to be entered
    mass_car = StringField('Car Mass ('+str(rm25_data['mass_car'])+')')
    mass_driver = StringField('Driver Mass ('+str(rm25_data['mass_driver'])+')')
    proportion_front = StringField('Proportion Front ('+str(rm25_data['proportion_front'])+')')
    front_track_width = StringField('Front Track Width ('+str(rm25_data['front_track_width'])+')')
    rear_track_width = StringField('Rear Track Width ('+str(rm25_data['rear_track_width'])+')')
    wheelbase = StringField('Wheelbase ('+str(rm25_data['wheelbase'])+')')
    CG_height = StringField('Center of Gravity Height ('+str(rm25_data['CG_height'])+')')
    yaw_inertia = StringField('Yaw Inertia ('+str(rm25_data['yaw_inertia'])+')')
    CoF = StringField('Coefficient of Friction ('+str(rm25_data['CoF'])+')')
    load_sensitivity = StringField('Load Sensitivity ('+str(rm25_data['load_sensitivity'])+')')
    Cd = StringField('Coefficient of Drag ('+str(rm25_data['Cd'])+')')
    Cl = StringField('Coefficient of Lift ('+str(rm25_data['Cl'])+')')
    A = StringField('Frontal Area ('+str(rm25_data['A'])+')')
    rho = StringField('Rho ('+str(rm25_data['rho'])+')')
    front_downforce = StringField('Front Downforce ('+str(rm25_data['front_downforce'])+')')
    cp_height = StringField('Center of Pressure Height ('+str(rm25_data['cp_height'])+')')
    brake_bias = StringField('Brake Bias ('+str(rm25_data['brake_bias'])+')')
    primary_drive = StringField('Primary Drive ('+str(rm25_data['primary_drive'])+')')
    engine_sprocket_teeth = StringField('Engine Sprocket Teeth ('+str(rm25_data['engine_sprocket_teeth'])+')')
    diff_sprocket_teeth = StringField('Diff Sprocket Teeth ('+str(rm25_data['diff_sprocket_teeth'])+')')
    tire_radius = StringField('Tire Radius ('+str(rm25_data['tire_radius'])+')')
    gear_ratios = StringField('Gear Ratios ('+str(rm25_data['gear_ratios'])+')')
    submit = SubmitField('Calculate')

class straightLineForm26(FlaskForm):

    directory = os.getcwd()
    rm26_data = json.loads(open(directory+"\\rm26.json").read())

    #each field for data to be entered
    mass_car = StringField('Car Mass ('+str(rm26_data['mass_car'])+')')
    mass_driver = StringField('Driver Mass ('+str(rm26_data['mass_driver'])+')')
    proportion_front = StringField('Proportion Front ('+str(rm26_data['proportion_front'])+')')
    front_track_width = StringField('Front Track Width ('+str(rm26_data['front_track_width'])+')')
    rear_track_width = StringField('Rear Track Width ('+str(rm26_data['rear_track_width'])+')')
    wheelbase = StringField('Wheelbase ('+str(rm26_data['wheelbase'])+')')
    CG_height = StringField('Center of Gravity Height ('+str(rm26_data['CG_height'])+')')
    yaw_inertia = StringField('Yaw Inertia ('+str(rm26_data['yaw_inertia'])+')')
    CoF = StringField('Coefficient of Friction ('+str(rm26_data['CoF'])+')')
    load_sensitivity = StringField('Load Sensitivity ('+str(rm26_data['load_sensitivity'])+')')
    Cd = StringField('Coefficient of Drag ('+str(rm26_data['Cd'])+')')
    Cl = StringField('Coefficient of Lift ('+str(rm26_data['Cl'])+')')
    A = StringField('Frontal Area ('+str(rm26_data['A'])+')')
    rho = StringField('Rho ('+str(rm26_data['rho'])+')')
    front_downforce = StringField('Front Downforce ('+str(rm26_data['front_downforce'])+')')
    cp_height = StringField('Center of Pressure Height ('+str(rm26_data['cp_height'])+')')
    brake_bias = StringField('Brake Bias ('+str(rm26_data['brake_bias'])+')')
    primary_drive = StringField('Primary Drive ('+str(rm26_data['primary_drive'])+')')
    engine_sprocket_teeth = StringField('Engine Sprocket Teeth ('+str(rm26_data['engine_sprocket_teeth'])+')')
    diff_sprocket_teeth = StringField('Diff Sprocket Teeth ('+str(rm26_data['diff_sprocket_teeth'])+')')
    tire_radius = StringField('Tire Radius ('+str(rm26_data['tire_radius'])+')')
    gear_ratios = StringField('Gear Ratios ('+str(rm26_data['gear_ratios'])+')')
    submit = SubmitField('Calculate')