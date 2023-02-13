from classes.car_simple import Car
import json

def test_func(data):
    if not data:
        print("No data")
    else:
        # json_data = json.loads(data)
        car = Car(data)