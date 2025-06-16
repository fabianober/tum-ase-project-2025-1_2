import random
import pandas as pd

# Parameters for the optimization 
rfPosScaling = 100
rfNegScaling = 200
weightScaling = 20
RF_goal = 1.05


# Assign the RF a score 
def rf_score(row):
    if row['Reserve Factor'] < 1:
        score = rfNegScaling * abs(row['Reserve Factor'] -RF_goal)
    else: 
        score = rfPosScaling * abs(row['Reserve Factor'] -RF_goal)
    return score

# Extracts the panel thickness from the stringer dataframe 
def extractThickness(df):
    thicknesses = []
    for i in range(1,6):
        thicknesses.append(df.thickness[i])
    return thicknesses

# Extracts dim1 until dim4 from stringer dataframe 
def extractDimensions(df):
    dimensions = []
    for i in range(0,5):
        dimensions.append([df.dim1[i], df.dim2[i], df.dim3[i], df.dim4[i]])
    return dimensions


def randomizeParameters(panelThickness, stringerDims):
    newPanelThickness = []
    for t in panelThickness:
        change = random.randint(-30, 30)/100
        newPanelThickness.append(t+change)
    newStringerDims = []
    for stringer in stringerDims:
        newStDim = []
        for dim in stringer:
            change = random.randint(-30, 30)/100
            newStDim.append(dim+change)
        newStringerDims.append(newStDim)
    return newPanelThickness, newStringerDims 
