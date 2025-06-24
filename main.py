
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

model = hm.Model()

'''Parameters for running the generational algorithm'''
NumGenerations = 2
NumChildren = 2
NumReverse = 1 # beacuse we found out, nothing changes after the first reverse iteration
RFgoal = 0.9

# get the rounding_digits from the ini file
config = configparser.ConfigParser()
config.read('./config.ini')
rounding_digits = int(config['DEFAULT']['rounding_digits'])

print("Getting your name...")

with open("name.txt", "r") as f:
    name = f.read().strip()

print(f"Your name is: {name}")

# For now create the score of the originial model 
#run_get_properties(name=name)
#run_run_analysis(name=name)
#calculate_panels(name=name)
#calculate_stringers(name=name)
#oneScoreDf(name=name, index=0)

# Here the generational algorithm is run 
def resetAll(name):
    changeParameters([4.0,4.0,4.0,4.0,4.0],[[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]])
    run_get_properties(name=name)
    run_run_analysis(name=name)
    run_get_stresses(name=name)
    calculate_panels(name=name)
    calculate_stringers(name=name)



# Reverse engineering 
def reverse(RFgoal_in):
    # Recalculate current state 
    run_get_properties(name=name)
    run_run_analysis(name=name)
    run_get_stresses(name=name)
    calculate_panels(name=name, RFgoal=RFgoal_in)
    calculate_stringers(name=name, RFgoal=RFgoal_in)

    for i in range(NumReverse):

        # For security, we check if we want to abbort. We read the file every time to ensure we catch any changes.
        with open("abort.bye", "r") as f:
            abort = f.read().strip()
        if abort == "1":
            print("Aborting the reverse algorithm. Bye...")
            sys.exit()

        print(f"Reverse iteration with RFgoal: {RFgoal_in}")
        newThick, newStringerDims = assembleUpdate(name)
        #print(newThick)
        changeParameters(newThick, newStringerDims)
        run_get_properties(name=name)
        run_run_analysis(name=name)
        run_get_stresses(name=name)
        calculate_panels(name=name, RFgoal=RFgoal_in)
        calculate_stringers(name=name, RFgoal=RFgoal_in)
        addScore(name=name)
    return None 

def evolution():

    # call reverse() here with RF_goal from 0.9 onwards

    try:
        generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
        bestPanelThickBefore = ast.literal_eval(generationDf['panel thickness'][0])
        bestStringerDimBefore = ast.literal_eval(generationDf['stringer Parameters'][0])
    except:
        bestPanelThickBefore = [4.0, 4.0, 4.0, 4.0, 4.0]
        bestStringerDimBefore = [[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]]

    for RFgoal in np.arange(1, 1.1, 0.05): # we have to set the range to 11 because we want to run it from 0.9 to 1.0
        changeParameters(bestPanelThickBefore, bestStringerDimBefore)  # Set the initial parameters before starting the evolution
        reverse(RFgoal_in=RFgoal)

    total_children = NumGenerations * NumChildren
    child_times = []
    children_done = 0
    generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
    generationDf = generationDf.sort_values(by='score', ascending=True).reset_index(drop=True)
    currentIndex = generationDf['GenIndex'].max()
    for i in range(0, NumGenerations):
        gen_start_time = time.time()
        generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
        panelThick = ast.literal_eval(generationDf['panel thickness'][0])
        StringerDim = ast.literal_eval(generationDf['stringer Parameters'][0])
        for j in range(0, NumChildren):
        
            # For security, we check if we want to abbort. We read the file every time to ensure we catch any changes.
            with open("abort.bye", "r") as f:
                abort = f.read().strip()
            if abort == "1":
                print("Aborting the generational algorithm. Bye...")
                sys.exit()
    
            child_start_time = time.time()
            newpanelThick, newStringerDim = randomizeParameters(panelThickness=panelThick, stringerDims=StringerDim)
            changeParameters(newpanelThick, newStringerDim)
            run_get_properties(name=name)
            run_run_analysis(name=name)
            run_get_stresses(name=name)
            calculate_panels(name=name)
            calculate_stringers(name=name)
            combinedScore(name=name, index=currentIndex+i+1)
            progress = ((i * NumChildren + (j + 1)) / (NumGenerations * NumChildren)) * 100
            child_end_time = time.time()
            child_duration = child_end_time - child_start_time
            child_times.append(child_duration)
            children_done += 1
            # Estimate remaining time
            avg_child_time = sum(child_times) / len(child_times)
            children_left = total_children - children_done
            remaining_time = avg_child_time * children_left
            rem_h = int(remaining_time // 3600)
            rem_m = int((remaining_time % 3600) // 60)
            rem_s = int(remaining_time % 60)
            print(f'CHILD {j+1}/{NumChildren} gen{i+1}/{NumGenerations} DONE | {progress:.1f}% | Time: {child_duration:.2f} s | Remaining: {rem_h}h {rem_m}m {rem_s}s')
           
        generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
        scoreDf = pd.read_csv(f'./data/{name}/output/children.csv')
        min_row = scoreDf.loc[scoreDf['score'].idxmin()]
        min_row = min_row.to_frame().T
        generationDf = pd.concat([generationDf, min_row], axis=0)
        generationDf = generationDf.sort_values(by='score', ascending=True).reset_index(drop=True)
        generationDf.to_csv(f'./data/{name}/output/generations.csv', index=False)
    
        # Delete the children.csv file to avoid confusion
        children_file = f'./data/{name}/output/children.csv'
        if os.path.exists(children_file):
            os.remove(children_file)
    
        gen_end_time = time.time()
        gen_duration = gen_end_time - gen_start_time
        print(f'GENERATION {i+1}/{NumGenerations} DONE | Time: {gen_duration:.2f} s')
        #reverse(RFgoal_in=0.9)  # Call reverse with the current RFgoal
        
    print("We now take your best results and set the properties in the model to those values")
    bestPanelThick = ast.literal_eval(generationDf['panel thickness'][0])
    bestStringerDim = ast.literal_eval(generationDf['stringer Parameters'][0])
    bestPanelThick = np.round(bestPanelThick, rounding_digits)
    bestStringerDim = np.round(bestStringerDim, rounding_digits)
    print(f"Your best panel thickness: {bestPanelThick}")
    print(f"Your best stringer dimensions: {bestStringerDim}")
    print("Setting the model to these values...")
    changeParameters(bestPanelThick, bestStringerDim)
    run_get_properties(name=name)
    run_run_analysis(name=name)
    run_get_stresses(name=name)
    calculate_panels(name=name)
    calculate_stringers(name=name)
    calculate_strength(name=name)
    write_mass_to_file(name=name)
    print(f"Your current model mass is: {round(generationDf['mass'][0], 3)} kg whilst your limit mass is {personal_data_provider(name=name)[3]} kg")
    
       
#reverse()
evolution()
#resetAll(name=name)
#Run_Optimisation_Ad_V3()

def Test():
    print("starting test")
    input = [
        25,25,25,25,25,
        20,20,20,20,20,
        15,15,15,15,15,
        2,2,2,2,2,
        4,4,4,4,4
    ]
    print("initialised input")
    out = fem_evaluate_vector(input,"felix",1.05)
    print("Test complete")
    print(out)

#Test()

def testingFnc():
    # Call your evaluation function
    input = [28,28,28,29,29,        #Dim 1
             25,25,26,26,26,        # Dim 2
             6,6,6,6,6,             # Dim 3
             5,5,5,5,5,             # Dim 4
             5,4.8,5,5,5.5]  #Skin thicknesses
    print("Using the input:")
    print(input)
    print("The result is:")
    result = fem_evaluate_vector(input, "felix", 1.05)
    print(result)
    
    # Set your threshold
    threshold = 1.05

    # Assuming result is a tuple as in your output, and the "RFs" are arrays at index 1, 2, 3
    rfs = []
    for idx in [1, 2, 3]:
        arr = result[idx]
        if hasattr(arr, '__iter__'):  # just to be safe
            rfs.extend(arr)
    
    # Check if any RF is below the threshold
    any_below = any(rf < threshold for rf in rfs)
    
    if any_below:
        print(f"At least one RF is below the threshold of {threshold}!")
    else:
        print(f"All RFs are above the threshold of {threshold}.")

    return 0

#testingFnc()


from local_LHS import *
sampleAround = [
    # web_height_1..5
    28.56829483, 28.69685558, 29.13367782, 28.79480978, 28.05068107,
    # flange_width_1..5
    28.0740408, 23.73077397, 23.14150937, 27.29645083, 25.06054826,
    # lip_height_1..5
    6.018909193, 6.175778463, 6.402557275, 5.428070725, 5.960830957,
    # thickness_1..5
    4.482355788, 4.871969974, 4.888170621, 5.190968939, 4.58977607,
    # skin_thickness_1..5
    4.719701115, 4.891748513, 4.949048523, 4.871264935, 5.568025744
]
#localLHS(790, 0.05, sampleAround)


# For now we reset the parameters afterwards
#print('Resetting model-parameters to initial values...')
#changeParameters([4.0,4.0,4.0,4.0,4.0],[[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]])
