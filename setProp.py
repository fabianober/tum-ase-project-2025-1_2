
print("Initializing main script...")
print('-----------------------')


import os
import sys
import pandas as pd
import ast
import time
import numpy as np
# config parser
import configparser

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('hmscript'))
sys.path.insert(0, os.path.abspath('formulas'))
sys.path.insert(0, os.path.abspath('calculators'))
sys.path.insert(0, os.path.abspath('optimization'))

from get_properties import *
from run_analysis import *
from get_stresses import *
from change_properties import *
from mass import *
from calculate_panels import *
from calculate_stringers import *
from calculate_strength import *
from generation import *
from ReverseEngineering import *

from run_optimizer_adaptiveV3_6_fin import *

run_id = sys.argv[1]

model = hm.Model()

# get the rounding_digits from the ini file
config = configparser.ConfigParser()
config.read('./config.ini')
rounding_digits = int(config['DEFAULT']['rounding_digits'])

print("Getting your name...")

with open("name.txt", "r") as f:
    name = f.read().strip()

print(f"Your name is: {name}")

def set_for_runid(run_id):

    generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
    selected_row = generationDf[generationDf['GenIndex'] == int(run_id)].iloc[0]
    panelThick = ast.literal_eval(selected_row['panel thickness'])
    stringerDim = ast.literal_eval(selected_row['stringer Parameters'])
    panelThick = np.round(panelThick, rounding_digits)
    stringerDim = np.round(stringerDim, rounding_digits)
    print(f"Setting the model to stringer dimensions: {stringerDim}, panel thicknesses: {panelThick}")
    changeParameters(panelThick, stringerDim)
    writeOffset(name=name)
    run_get_properties(name=name)
    run_run_analysis(name=name)
    run_get_stresses(name=name)
    calculate_panels(name=name)
    calculate_stringers(name=name)
    calculate_strength(name=name)
    write_mass_to_file(name=name)

if __name__ == "__main__":
    print("Running setProp.py...")
    print(f'Your selected run ID is: {run_id}')
    set_for_runid(run_id)
    print("setProp.py finished.")
    print('-----------------------')