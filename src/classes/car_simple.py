import json


class Car:
    def __init__(self, car_file):
        # with open(car_file) as f:
            self.attrs = json.loads(car_file)
