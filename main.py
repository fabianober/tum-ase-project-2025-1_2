
print("Initializing main script...")
print('-----------------------')


import os
import sys
import pandas as pd
import ast
import time

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
from ReverseEngineering import *

from run_optimizer_adaptiveV3_6_fin import *

model = hm.Model()

'''Parameters for running the generational algorithm'''
NumGenerations = 10
NumChildren = 30
NumReverse = 2
RFgoal = 0.9

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
    calculate_panels(name=name)
    calculate_stringers(name=name, RFgoal=RFgoal_in)

    for i in range(NumReverse):

        # For security, we check if we want to abbort. We read the file every time to ensure we catch any changes.
        with open("abort.bye", "r") as f:
            abort = f.read().strip()
        if abort == "1":
            print("Aborting the reverse algorithm. Bye...")
            sys.exit()

        print(f"Reverse iteration {i+1}/{NumReverse} with RFgoal: {RFgoal_in}")
        newThick, newStringerDims = assembleUpdate(name)
        #print(newThick)
        changeParameters(newThick, newStringerDims)
        run_get_properties(name=name)
        run_run_analysis(name=name)
        run_get_stresses(name=name)
        calculate_panels(name=name)
        calculate_stringers(name=name, RFgoal=RFgoal_in)
        addScore(name=name)
    return None 

def evolution():

    # call reverse() here with RF_goal from 0.9 onwards
    for i in range(0, 11):
        RFgoal = 0.9 + i * 0.01
        #print(f"Running reverse with RFgoal: {RFgoal}")
        reverse(RFgoal_in=RFgoal)

    total_children = NumGenerations * NumChildren
    child_times = []
    children_done = 0
    generationDf = pd.read_csv(f'./data/{name}/output/generations.csv')
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


 # For now we reset the parameters afterwards
print('Resetting model-parameters to initial values...')
changeParameters([4.0,4.0,4.0,4.0,4.0],[[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]])
