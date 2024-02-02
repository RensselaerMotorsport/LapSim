import pandas as pd
import os

DIR = "RawData_DriveBrake_ASCII_SI"
FLN = os.scandir(DIR)

for i in FLN:
    print(pd.read_csv(DIR + "/" + i.name))
