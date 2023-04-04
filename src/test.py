from app.classes.car_simple import Car


def test_func(data):
    if not data:
        print("No data")
    else:
        car = Car(data)