from app.static.python_scripts.car_simple import Car
from app.static.python_scripts.helper_functions_ev import line_segment_time
import json

def test_func(data):
    if not data:
        print("No data")
    else:
        car = Car(data)