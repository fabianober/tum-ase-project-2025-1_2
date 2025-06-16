import random

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

def extractThickness(df):
    thicknesses = []
    for i in range(1,6):
        thicknesses.append(df.thickness[i])
    return thicknesses