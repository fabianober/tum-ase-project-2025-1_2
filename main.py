
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

cleaUp_before = sys.argv[1]

model = hm.Model()

'''Parameters for running the generational algorithm'''
NumGenerations = 20
NumChildren = 30
NumReverse = 1 # beacuse we found out, nothing changes after the first reverse iteration

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

if cleaUp_before == "1":
    output_dir = f'./data/{name}/output'
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            file_path = os.path.join(output_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

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

    for RFgoal in np.arange(1, 1.8, 0.05): # we have to set the range to 11 because we want to run it from 0.9 to 1.0
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
    writeOffset(name=name)
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
    input = [
        # web_height_1..5
        27.914523975811907, 29.933747987618634, 29.492292141671786, 27.920552008253434, 29.204732682250246,
        # flange_width_1..5
        28.704517455252248, 23.793185957009474, 22.68619758129179, 26.937227807439353, 23.53174361651497,
        # lip_height_1..5
        6.244956843610818, 6.638685425179286, 6.303537036611106, 5.438419149663298, 6.285980142103777,
        # thickness_1..5
        4.4312188202231635, 4.721923248997934, 5.21244851761281, 5.271239600298142, 4.403847396900568,
        # skin_thickness_1..5
        4.624397489061536, 4.823874380815895, 4.80428411028983, 4.827961626192825, 5.374514675054963
    ]
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
    31.83510184,   # web_height_1
    31.54595767,   # web_height_2
    27.79032774,   # web_height_3
    28.32766755,   # web_height_4
    28.72232605,   # web_height_5
    24.18102748,   # flange_width_1
    21.34641941,   # flange_width_2
    25.79735456,   # flange_width_3
    27.82647585,   # flange_width_4
    24.86176088,   # flange_width_5
    3.339564014,   # lip_height_1
    3.471299133,   # lip_height_2
    3.971518646,   # lip_height_3
    3.719669516,   # lip_height_4
    3.344856986,   # lip_height_5
    4.13737146,    # thickness_1
    4.53336267,    # thickness_2
    5.297966049,   # thickness_3
    4.871718032,   # thickness_4
    4.819117425,   # thickness_5
    5.405379871,   # skin_thickness_1
    5.533845505,   # skin_thickness_2
    4.979328327,   # skin_thickness_3
    5.189326628,   # skin_thickness_4
    5.837596609    # skin_thickness_5
]

#localLHS(550, 0.05, sampleAround)


localLHS_variable_spread(
    400,
    #[0.03]*25,  # or your specific spread values,
    [0.03,0.03,0.03,0.03,0.03, 0.03,0.03,0.03,0.03,0.03, 0.03,0.03,0.03,0.03,0.03, 0.2,0.2,0.2,0.2,0.2, 0.04,0.04,0.04,0.04,0.04]
    [
    # web_height_1-5
    38.69355189, 38.84872184, 39.14653229, 39.01926354, 39.21231119,
    # flange_width_1-5
    26.80288089, 29.47964875, 28.08588948, 28.73329173, 28.5486787,
    # lip_height_1-5
    16.03872922, 14.40906127, 14.74787211, 14.43297435, 15.28101159,
    # thickness_1-5
    1.63851838, 1.559057955, 1.552564539, 1.596815243, 1.465323414,
    # skin_thickness_1-5
    5.149498813, 5.064777061, 5.008728829, 5.526816236, 6.141245415
    ],
    output_csv="lhs_results_24.csv"
)


# Bin (0, 0)
sampleAround_custom = (
    [
        36.26805304207083, 39.66056707303221, 38.865188184356, 38.69708136808374, 40.05376307985308,  # web_height_1-5
        28.83993400772921, 27.69531949138326, 30.0212740800636, 30.50931776531474, 31.6648612301249,   # flange_width_1-5
        14.91149105513435, 14.0045438933091, 15.61620001102858, 14.12502156886974, 14.86998251895254,  # lip_height_1-5
        1.70256305723931, 1.46869968466406, 1.542924183185306, 1.681658735937442, 1.545606182064441,   # thickness_1-5
        4.86844901169275, 5.147278121528451, 5.047634478330306, 5.262489487887247, 5.91699215753789    # skin_thickness_1-5
    ]
)

#localLHS(400, 0.7, sampleAround_custom)

# Bin (0, 1)
sampleAround_01 = (
    [28.14]*5 +
    [25.13]*5 +
    [3.80]*5 +
    [4.83]*5 +
    [5.65]*5
)
#localLHS2(140, 0.10, sampleAround_01)

# Bin (0, 2)
sampleAround_02 = (
    [28.14]*5 +
    [25.13]*5 +
    [3.80]*5 +
    [4.83]*5 +
    [6.75]*5
)
#localLHS3(140, 0.10, sampleAround_02)

# Bin (0, 3)
sampleAround_03 = (
    [28.14]*5 +
    [25.13]*5 +
    [3.80]*5 +
    [4.83]*5 +
    [7.85]*5
)
#localLHS4(140, 0.10, sampleAround_03)

# Bin (0, 4)
sampleAround_04 = (
    [28.14]*5 +
    [25.13]*5 +
    [3.80]*5 +
    [4.83]*5 +
    [8.95]*5
)
#localLHS5(140, 0.10, sampleAround_04)




# For now we reset the parameters afterwards
#print('Resetting model-parameters to initial values...')
#changeParameters([4.0,4.0,4.0,4.0,4.0],[[25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15], [25,2,20,15]])
