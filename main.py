
print("Initializing main script...")
print('-----------------------')

import os
import sys
import pandas as pd
import ast

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
from generation import *

model = hm.Model()

'''Parameters for running the generational algorithm'''
NumGenerations = 1
NumChildren = 2


print("Getting your name...")

with open("name.txt", "r") as f:
    name = f.read().strip()

print(f"Your name is: {name}")


# Uncomment if needed 

"""# run get_properties
print('-----------------------')
print('Running get_properties...')
run_get_properties(name=name)

# run analysis and clean up
print('-----------------------')
print('Running run_run_analysis...')
run_run_analysis(name=name)


# get stresses
print('-----------------------')
print('Running run_run_analysis...')
run_get_stresses(name=name)

# run our scripts
print('-----------------------')
print('We have successfully run the hm analysis and can now run the calculators')
print('Running mass calculator...')
total_mass = total_mass(name=name)
print(f"Total mass of the structure: {total_mass} kg")

print('-----------------------')
print('Running panels calculator...')
calculate_panels(name=name)


print('-----------------------')
print('Running stringers calculator...')
calculate_stringers(name=name)"""






# For now create the score of the originial model 
run_get_properties(name=name)
run_run_analysis(name=name)
calculate_panels(name=name)
calculate_stringers(name=name)
oneScoreDf(name=name)


# Here the generational algorithm is run 
for i in range(0,NumGenerations):
    generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
    panelThick = ast.literal_eval(generationDf['panel thickness'][0])
    StringerDim = ast.literal_eval(generationDf['stringer Parameters'][0])
    for j in range(0, NumChildren):
        newpanelThick, newStringerDim = randomizeParameters(panelThickness = panelThick, stringerDims = StringerDim)
        changeParameters(newpanelThick, newStringerDim)
        run_get_properties(name=name)
        run_run_analysis(name=name)
        calculate_panels(name=name)
        calculate_stringers(name=name)
        combinedScore(name=name)
    print('FIRST GENERATION DONE')
    generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
    scoreDf = pd.read_csv(f'./data/{name}/output/children.csv')
    min_row = scoreDf.loc[scoreDf['score'].idxmin()]
    min_row = min_row.to_frame().T
    generationDf=pd.concat([generationDf, min_row], axis=0)
    generationDf = generationDf.sort_values(by='score', ascending=True).reset_index(drop=True)
    generationDf.to_csv(f'./data/{name}/output/generations.csv', index=False)


# For now we reset the parameters afterwards
changeParameters([4.0,4.0,4.0,4.0,4.0],[[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]])
