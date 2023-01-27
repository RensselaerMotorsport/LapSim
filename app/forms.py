from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import json

#CHANGE THIS TO PROPER DIRECTORY BEFORE DEPLOYMENT
rm25_data = json.loads(open('C:\\Users\\fornem\\Dropbox\\lapsim\\lapsim_final\\rm25.json').read())
rm26_data = json.loads(open('C:\\Users\\fornem\\Dropbox\\lapsim\\lapsim_final\\rm26.json').read())

#each perimeter from the json file if the user wants to change them
#no data is required
class straightLineForm25(FlaskForm):
    mass_car = StringField('Car Mass'+str(rm25_data['mass_car'])+')')
    mass_driver = StringField('Driver Mass ('+str(rm25_data['mass_driver'])+')')
    proportion_front = StringField('Proportion Front (',rm25_data['proportion_front'],')')
    front_track_width = StringField('Front Track Width (',rm25_data['front_track_width'],')')
    rear_track_width = StringField('Rear Track Width (',rm25_data['rear_track_width'],')')
    wheelbase = StringField('Wheelbase (',rm25_data['wheelbase'],')')
    CG_height = StringField('Center of Gravity Height (',rm25_data['CG_height'],')')
    yaw_inertia = StringField('Yaw Inertia (',rm25_data['yaw_inertia'],')')
    CoF = StringField('Coefficient of Friction (',rm25_data['CoF'],')')
    load_sensitivity = StringField('Load Sensitivity (',rm25_data['load_sensitivity'],')')
    Cd = StringField('Coefficient of Drag (',rm25_data['Cd'],')')
    Cl = StringField('Coefficient of Lift (',rm25_data['Cl'],')')
    A = StringField('Frontal Area (',rm25_data['A'],')')
    rho = StringField('Rho (',rm25_data['rho'],')')
    front_downforce = StringField('Front Downforce (',rm25_data['front_downforce'],')')
    cp_height = StringField('Center of Pressure Height (',rm25_data['cp_height'],')')
    brake_bias = StringField('Brake Bias (',rm25_data['brake_bias'],')')
    rimary_drive = StringField('Primary Drive (',rm25_data['primary_drive'],')')
    engine_sprocket_teeth = StringField('Engine Sprocket Teeth (',rm25_data['engine_sprocket_teeth'],')')
    diff_sprocket_teeth = StringField('Diff Sprocket Teeth (',rm25_data['diff_sprocket_teeth'],')')
    tire_radius = StringField('Tire Radius (',rm25_data['tire_radius'],')')
    gear_ratios = StringField('Gear Ratios (',rm25_data['gear_ratios'],')')
    submit = SubmitField('Calculate')

'''class straightLineForm26(FlaskForm):
    submit = SubmitField('Calculate')
    mass_car = StringField('Car Mass (',rm26_data['mass_car'],')')
    mass_driver = StringField('Driver Mass (',rm26_data['mass_driver'],')')
    proportion_front = StringField('Proportion Front (',rm26_data['proportion_front'],')')
    front_track_width = StringField('Front Track Width (',rm26_data['front_track_width'],')')
    rear_track_width = StringField('Rear Track Width (',rm26_data['rear_track_width'],')')
    wheelbase = StringField('Wheelbase (',rm26_data['wheelbase'],')')
    CG_height = StringField('Center of Gravity Height (',rm26_data['CG_height'],')')
    yaw_inertia = StringField('Yaw Inertia (',rm26_data['yaw_inertia'],')')
    CoF = StringField('Coefficient of Friction (',rm26_data['CoF'],')')
    load_sensitivity = StringField('Load Sensitivity (',rm26_data['load_sensitivity'],')')
    Cd = StringField('Coefficient of Drag (',rm26_data['Cd'],')')
    Cl = StringField('Coefficient of Lift (',rm26_data['Cl'],')')
    A = StringField('Frontal Area (',rm26_data['A'],')')
    rho = StringField('Rho (',rm26_data['rho'],')')
    front_downforce = StringField('Front Downforce (',rm26_data['front_downforce'],')')
    cp_height = StringField('Center of Pressure Height (',rm26_data['cp_height'],')')
    brake_bias = StringField('Brake Bias (',rm26_data['brake_bias'],')')
    primary_drive = StringField('Primary Drive (',rm26_data['primary_drive'],')')
    engine_sprocket_teeth = StringField('Engine Sprocket Teeth (',rm26_data['engine_sprocket_teeth'],')')
    diff_sprocket_teeth = StringField('Diff Sprocket Teeth (',rm26_data['diff_sprocket_teeth'],')')
    tire_radius = StringField('Tire Radius (',rm26_data['tire_radius'],')')
    gear_ratios = StringField('Gear Ratios (',rm26_data['gear_ratios'],')')'''