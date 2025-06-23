import random
import pandas as pd
import ast
import sys 
import os


# Join paths for own modules 
sys.path.insert(0, os.path.abspath('..')) 
sys.path.insert(0, os.path.abspath('formulas'))
#Import own modules 
from mass import *
from helpers import *


# Parameters for the optimization 
rfPosScaling = 5
rfNegScaling = 500
NegweightScaling = 850
PosweightScaling = 1
RF_goal = 1.05


# Assign the RF a score 
def rf_score(row):
    if row['Reserve Factor'] < 1:
        score = pow(rfNegScaling * abs(row['Reserve Factor'] -RF_goal), 2)
    else: 
        score = pow(rfPosScaling * abs(row['Reserve Factor'] -RF_goal), 2)
    return score

# mass score 
def massScoreCalc(name):
    maxMass = personal_data_provider(name)[3]  # Get the max mass from the personal data provider
    tot_mass = total_mass(name=name)
    clearance = maxMass-tot_mass
    if clearance <= 0:
        massScore = pow(abs(clearance) * NegweightScaling, 2)
    else:
        massScore = pow((1/clearance) * PosweightScaling, 2)
    return tot_mass, massScore 



# Extracts the panel thickness from the stringer dataframe 
def extractThickness(df):
    thicknesses = []
    for i in range(1,6):
        thicknesses.append(float(df.thickness[i]))
    return thicknesses

# Extracts dim1 until dim4 from stringer dataframe 
def extractDimensions(df):
    dimensions = []
    for i in range(0,5):
        dimensions.append([float(df.dim1[i]), float(df.dim2[i]), float(df.dim3[i]), float(df.dim4[i])])
    return dimensions

# Randomizes the input parameters 
def randomizeParameters(panelThickness, stringerDims):
    newPanelThickness = []
    for t in panelThickness:
        t = float(t)
        change = random.randint(-30, 30)/100
        newPanelThickness.append(t + change)
    newStringerDims = []
    for stringer in stringerDims:
        newStDim = []
        for dim in stringer:
            dim = float(dim)
            change = random.randint(-30, 30)/100
            newStDim.append(dim+change)
        newStringerDims.append(newStDim)
    return newPanelThickness, newStringerDims 

# Compute and append the score of one iteration
def combinedScore(name, index):
    # Import already existing iterations
    try:
        #print("Doing the correct thing")
        scoreDf = pd.read_csv(f'./data/{name}/output/children.csv')
        # Import files to compute new score 
        panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
        stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
        total_mass, massScore = massScoreCalc(name)
        minRF = min(panelScoreDf['minRF'][0], stringerScoreDf['minRF'][0])
        # Concat to one new parameter score entry
        newscoreDf = pd.DataFrame({
            'panel thickness':[panelScoreDf['panel thickness'][0]],
            'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
            'mass':[total_mass],
            'min RF': [minRF],
            'GenIndex':[index],
            'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
            
        })

        scoreDf=pd.concat([scoreDf, newscoreDf], axis=0)
        scoreDf.to_csv(f'./data/{name}/output/children.csv', index=False)
    except:
        #print("Doing the initial step")
        # Import files to compute new score 
        panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
        stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
        total_mass, massScore = massScoreCalc(name)
        minRF = min(panelScoreDf['minRF'][0], stringerScoreDf['minRF'][0])
        # Concat to one new parameter score entry
        newscoreDf = pd.DataFrame({
            'panel thickness':[panelScoreDf['panel thickness'][0]],
            'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
            'mass':[total_mass],
            'min RF': [minRF],
            'GenIndex':[index],
            'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
            
        })
        newscoreDf.to_csv(f'./data/{name}/output/children.csv', index=False)
    return None 


# Adds the scores of the reverse Engineering part 
def addScore(name):
    try:
        #print("Doing the correct thing")
        scoreDf = pd.read_csv(f'./data/{name}/output/generations.csv')
        # Import files to compute new score 
        panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
        stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
        total_mass, massScore = massScoreCalc(name)
        minRF = min(panelScoreDf['minRF'][0], stringerScoreDf['minRF'][0])
        # Concat to one new parameter score entry
        newscoreDf = pd.DataFrame({
            'panel thickness':[panelScoreDf['panel thickness'][0]],
            'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
            'mass':[total_mass],
            'min RF': [minRF],
            'GenIndex':[scoreDf['GenIndex'].max()+1],
            'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
            
        })

        scoreDf=pd.concat([scoreDf, newscoreDf], axis=0)
        scoreDf = scoreDf.sort_values(by='score', ascending=True).reset_index(drop=True)
        scoreDf.to_csv(f'./data/{name}/output/generations.csv', index=False)
        

    except:
        # Import files to compute new score if no one before existed 
        panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
        stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
        total_mass, massScore = massScoreCalc(name)
        minRF = min(panelScoreDf['minRF'][0], stringerScoreDf['minRF'][0])
        # Concat to one new parameter score entry
        newscoreDf = pd.DataFrame({
                'panel thickness':[panelScoreDf['panel thickness'][0]],
                'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
                'mass':[total_mass],
                'min RF': [minRF],
                'GenIndex':[0],
                'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
            
            })
        newscoreDf.to_csv(f'./data/{name}/output/generations.csv', index=False)
    return None





def oneScoreDf(name, index):
    # Import files to compute new score 
    panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
    stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
    total_mass, massScore = massScoreCalc(name)
    minRF = min(panelScoreDf['minRF'][0], stringerScoreDf['minRF'][0])
    # Concat to one new parameter score entry
    newscoreDf = pd.DataFrame({
            'panel thickness':[panelScoreDf['panel thickness'][0]],
            'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
            'mass':[total_mass],
            'min RF': [minRF],
            'GenIndex':[index],
            'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
            
        })
    newscoreDf.to_csv(f'./data/{name}/output/generations.csv', index=False)
    return None
#combinedScore(name='yannis')
