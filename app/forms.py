from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
import json #car data
import os #get current working directory for json file

#each perimeter from the json file if the user wants to change them
#no data is required, a blank field should use the json data
#the data returned from these forms will be plugged into the helper functions (need to figure out how to incorporate those)
#helper functions and straight line sim program are found in src branch of repo
class straightLineForm25(FlaskForm):

    directory = os.getcwd()
    rm25_data = json.loads(open(directory+"\\app\\rm25.json").read())

    #each field for data to be entered
    mass_car = DecimalField('Car Mass ('+str(rm25_data['mass_car'])+')')
    mass_car_begin = DecimalField('Car Mass Begin')
    mass_car_end = DecimalField('Car Mass End')
    mass_car_step = DecimalField('Car Mass Step')

    mass_driver = DecimalField('Driver Mass ('+str(rm25_data['mass_driver'])+')')
    mass_driver_begin = DecimalField('Driver Mass Begin')
    mass_driver_end = DecimalField('Driver Mass End')
    mass_driver_step = DecimalField('Driver Mass Step')

    proportion_front = DecimalField('Proportion Front ('+str(rm25_data['proportion_front'])+')')
    proportion_front_begin = DecimalField('Proportion Front Begin')
    proportion_front_end = DecimalField('Proportion Front End')
    proportion_front_step = DecimalField('Proportion Front Step')

    front_track_width = DecimalField('Front Track Width ('+str(rm25_data['front_track_width'])+')')
    front_track_width_begin = DecimalField('Front Track Width Begin')
    front_track_width_end = DecimalField('Front Track Width End')
    front_track_width_step = DecimalField('Front Track Width Step')

    rear_track_width = DecimalField('Rear Track Width ('+str(rm25_data['rear_track_width'])+')')
    rear_track_width_begin = DecimalField('Rear Track Width Begin')
    rear_track_width_end = DecimalField('Rear Track Width End')
    rear_track_width_step = DecimalField('Rear Track Width Step')

    wheelbase = DecimalField('Wheelbase ('+str(rm25_data['wheelbase'])+')')
    wheelbase_begin = DecimalField('Wheelbase Begin')
    wheelbase_end = DecimalField('Wheelbase End')
    wheelbase_step = DecimalField('Wheelbase Step')

    CG_height = DecimalField('Center of Gravity Height ('+str(rm25_data['CG_height'])+')')
    CG_height_begin = DecimalField('Center of Gravity Height Begin')
    CG_height_end = DecimalField('Center of Gravity Height End')
    CG_height_step = DecimalField('Center of Gravity Height Step')

    yaw_inertia = DecimalField('Yaw Inertia ('+str(rm25_data['yaw_inertia'])+')')
    yaw_inertia_begin = DecimalField('Yaw Inertia Begin')
    yaw_inertia_end = DecimalField('Yaw Inertia End')
    yaw_inertia_step = DecimalField('Yaw Inertia Step')

    CoF = DecimalField('Coefficient of Friction ('+str(rm25_data['CoF'])+')')
    CoF_begin = DecimalField('Coefficient of Friction Begin')
    CoF_end = DecimalField('Coefficient of Friction End')
    CoF_step = DecimalField('Coefficient of Friction Step')

    load_sensitivity = DecimalField('Load Sensitivity ('+str(rm25_data['load_sensitivity'])+')')
    load_sensitivity_begin = DecimalField('Load Sensitivity Begin')
    load_sensitivity_end = DecimalField('Load Sensitivity End')
    load_sensitivity_step = DecimalField('Load Sensitivity Step')

    Cd = DecimalField('Coefficient of Drag ('+str(rm25_data['Cd'])+')')
    Cd_begin = DecimalField('Coefficient of Drag Begin')
    Cd_end = DecimalField('Coefficient of Drag End')
    Cd_step = DecimalField('Coefficient of Drag Step')

    Cl = DecimalField('Coefficient of Lift ('+str(rm25_data['Cl'])+')')
    Cl_begin = DecimalField('Coefficient of Lift Begin')
    Cl_end = DecimalField('Coefficient of Lift End')
    Cl_step = DecimalField('Coefficient of Lift Step')

    A = DecimalField('Frontal Area ('+str(rm25_data['A'])+')')
    A_begin = DecimalField('Frontal Area Begin')
    A_end = DecimalField('Frontal Area End')
    A_step = DecimalField('Frontal Area Step')

    rho = DecimalField('Rho ('+str(rm25_data['rho'])+')')
    rho_begin = DecimalField('Rho Begin')
    rho_end = DecimalField('Rho End')
    rho_step = DecimalField('Rho Step')

    front_downforce = DecimalField('Front Downforce ('+str(rm25_data['front_downforce'])+')')
    front_downforce_begin = DecimalField('Front Downforce Begin')
    front_downforce_end = DecimalField('Front Downforce End')
    front_downforce_step = DecimalField('Front Downforce Step')

    cp_height = DecimalField('Center of Pressure Height ('+str(rm25_data['cp_height'])+')')
    cp_height_begin = DecimalField('Center of Pressure Height Begin')
    cp_height_end = DecimalField('Center of Pressure Height End')
    cp_height_step = DecimalField('Center of Pressure Height Step')

    brake_bias = DecimalField('Brake Bias ('+str(rm25_data['brake_bias'])+')')
    brake_bias_begin = DecimalField('Brake Bias Begin')
    brake_bias_end = DecimalField('Brake Bias End')
    brake_bias_step = DecimalField('Brake Bias Step')

    primary_drive = DecimalField('Primary Drive ('+str(rm25_data['primary_drive'])+')')
    primary_drive_begin = DecimalField('Primary Drive Begin')
    primary_drive_end = DecimalField('Primary Drive End')
    primary_drive_step = DecimalField('Primary Drive Step')

    engine_sprocket_teeth = DecimalField('Engine Sprocket Teeth ('+str(rm25_data['engine_sprocket_teeth'])+')')
    engine_sprocket_teeth_begin = DecimalField('Engine Sprocket Teeth Begin')
    engine_sprocket_teeth_end = DecimalField('Engine Sprocket Teeth End')
    engine_sprocket_teeth_step = DecimalField('Engine Sprocket Teeth Step')

    diff_sprocket_teeth = DecimalField('Diff Sprocket Teeth ('+str(rm25_data['diff_sprocket_teeth'])+')')
    diff_sprocket_teeth_begin = DecimalField('Diff Sprocket Teeth Begin')
    diff_sprocket_teeth_end = DecimalField('Diff Sprocket Teeth End')
    diff_sprocket_teeth_step = DecimalField('Diff Sprocket Teeth Step')

    tire_radius = DecimalField('Tire Radius ('+str(rm25_data['tire_radius'])+')')
    tire_radius_begin = DecimalField('Tire Radius Begin')
    tire_radius_end = DecimalField('Tire Radius End')
    tire_radius_step = DecimalField('Tire Radius Step')

    gear_ratios = StringField('Gear Ratios; enter values as a comma separated list ('+str(rm25_data['gear_ratios']).lstrip('[').rstrip(']')+')')
    gear_ratios_begin = StringField('Gear Ratios Begin; enter values as a comma separated list')
    gear_ratios_end = StringField('Gear Ratios End; enter values as a comma separated list')
    gear_ratios_step = StringField('Gear Ratios Step; enter values as a comma separated list')

    submit = SubmitField('Calculate')

class straightLineForm26(FlaskForm):

    directory = os.getcwd()
    rm26_data = json.loads(open(directory+"\\app\\rm26.json").read())

    #each field for data to be entered
    mass_car = DecimalField('Car Mass ('+str(rm26_data['mass_car'])+')')
    mass_driver = DecimalField('Driver Mass ('+str(rm26_data['mass_driver'])+')')
    proportion_front = DecimalField('Proportion Front ('+str(rm26_data['proportion_front'])+')')
    front_track_width = DecimalField('Front Track Width ('+str(rm26_data['front_track_width'])+')')
    rear_track_width = DecimalField('Rear Track Width ('+str(rm26_data['rear_track_width'])+')')
    wheelbase = DecimalField('Wheelbase ('+str(rm26_data['wheelbase'])+')')
    CG_height = DecimalField('Center of Gravity Height ('+str(rm26_data['CG_height'])+')')
    yaw_inertia = DecimalField('Yaw Inertia ('+str(rm26_data['yaw_inertia'])+')')
    CoF = DecimalField('Coefficient of Friction ('+str(rm26_data['CoF'])+')')
    load_sensitivity = DecimalField('Load Sensitivity ('+str(rm26_data['load_sensitivity'])+')')
    Cd = DecimalField('Coefficient of Drag ('+str(rm26_data['Cd'])+')')
    Cl = DecimalField('Coefficient of Lift ('+str(rm26_data['Cl'])+')')
    A = DecimalField('Frontal Area ('+str(rm26_data['A'])+')')
    rho = DecimalField('Rho ('+str(rm26_data['rho'])+')')
    front_downforce = DecimalField('Front Downforce ('+str(rm26_data['front_downforce'])+')')
    cp_height = DecimalField('Center of Pressure Height ('+str(rm26_data['cp_height'])+')')
    brake_bias = DecimalField('Brake Bias ('+str(rm26_data['brake_bias'])+')')
    primary_drive = DecimalField('Primary Drive ('+str(rm26_data['primary_drive'])+')')
    engine_sprocket_teeth = DecimalField('Engine Sprocket Teeth ('+str(rm26_data['engine_sprocket_teeth'])+')')
    diff_sprocket_teeth = DecimalField('Diff Sprocket Teeth ('+str(rm26_data['diff_sprocket_teeth'])+')')
    tire_radius = DecimalField('Tire Radius ('+str(rm26_data['tire_radius'])+')')
    gear_ratios = StringField('Gear Ratios; enter values as a comma separated list ('+str(rm26_data['gear_ratios']).lstrip('[').rstrip(']')+')')
    submit = SubmitField('Calculate')