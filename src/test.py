from classes.car_simple import Car
from helper_functions_ev import line_segment_time
import json

def test_func(data):
    if not data:
        print("No data")
    else:
        car = Car(data)