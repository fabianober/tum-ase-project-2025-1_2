# # Task 1 d, Calculating strength reserve factor of all elements

import pandas as pd
import sys 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '../formulas')))

from formulas.columnbuckling import *
from formulas.panels import *
from formulas.strength import *
from formulas.helpers import *
import configparser

# get the rounding_digits from the ini file
config = configparser.ConfigParser()
config.read('../config.ini')
rounding_digits = int(config['DEFAULT']['rounding_digits'])

def calculate_strength(name):
    # This will become the new import for the panel stresses
    paneldf = pd.read_csv(f'../data/{name}/panel.csv')
    stringerdf= pd.read_csv(f'../data/{name}/stringer.csv')

    sigma_ult = 530

    #Adding reserve Factor column to the panels 
    paneldf['reserveFactor'] = paneldf.apply(panelStrength_calc, sigma_ult= sigma_ult, axis=1)


    #Adding reserve Factor column to the stringers 
    stringerdf['reserveFactor'] = stringerdf.apply(stringerStrength_calc, sigma_ult= sigma_ult, axis=1)
    # ## Delete unnecessary columns 

    # First for the stringers 
    stringerdf = stringerdf.drop(['Component Name','sigmaXX'], axis=1)


    # Then also the panels 
    paneldf=paneldf.drop(['Component Name', 'sigmaXX', 'sigmaYY', 'sigmaXY'], axis = 1)

    # ## Concat data frames beneth each other 
    combined = pd.concat([paneldf,stringerdf],axis=0)

    # ## Split into three seperate loadcase data frames 
    loadCase1df = combined[combined['Load Case'] == 'Subcase 1 (LC1)']
    loadCase2df = combined[combined['Load Case'] == 'Subcase 2 (LC2)']
    loadCase3df = combined[combined['Load Case'] == 'Subcase 3 (LC3)']

    # Drop the loadcase columns 
    loadCase1df = loadCase1df.drop(['Load Case'], axis = 1)
    loadCase2df = loadCase2df.drop(['Load Case'], axis = 1)
    loadCase3df = loadCase3df.drop(['Load Case'], axis = 1)
    #Rename the reserveFactor column 
    loadCase1df = loadCase1df.rename(columns={"reserveFactor": "Load Case 1 RF"})
    loadCase2df = loadCase2df.rename(columns={"reserveFactor": "Load Case 2 RF"})
    loadCase3df = loadCase3df.rename(columns={"reserveFactor": "Load Case 3 RF"})
    # Make element ID index column 
    loadCase1df = loadCase1df.set_index('Element ID')
    loadCase2df = loadCase2df.set_index('Element ID')
    loadCase3df = loadCase3df.set_index('Element ID')

    # Now we concat them back together 
    outputdf = pd.concat([loadCase1df,loadCase2df, loadCase3df], axis=1)
    # # ROUND & Export back to Excel 
    outputdf = outputdf.round(rounding_digits)
    outputdf.to_excel(f'../data/{name}/output/processed_d.xlsx')

if __name__ == "__main__":
    calculate_strength('fabian')