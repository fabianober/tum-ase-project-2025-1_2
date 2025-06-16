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
# mass score 
def massScoreCalc():
    score = 0
    return score 



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

# Compute and append the score of one iteration
def combinedScore(name):
    # Import already existing iterations
    scoreDf = pd.read_csv(f'./data/{name}/output/generation.csv')
    # Import files to compute new score 
    panelScoreDf = pd.read_csv(f'./data/{name}/output/panelScore.csv')
    stringerScoreDf = pd.read_csv(f'./data/{name}/output/stringerScore.csv')
    massScore = massScoreCalc()
    # Concat to one new parameter score entry
    newscoreDf = pd.DataFrame({
        'panel thickness':[panelScoreDf['panel thickness'][0]],
        'stringer Parameters':[stringerScoreDf['stringer Parameters'][0]],
        'score':[massScore+panelScoreDf.score[0] + stringerScoreDf.score[0]]
    })

    scoreDf=pd.concat([scoreDf, newscoreDf], axis=0)
    scoreDf.to_csv(f'./data/{name}/output/generation.csv', index=False)
    return None 

combinedScore(name='yannis')
