import os 
import sys 
import pandas as pd 

# Join paths for own modules 
sys.path.insert(0, os.path.abspath('..')) 
sys.path.insert(0, os.path.abspath('formulas'))

from panelBuckReverse import *
from columnBuckReverse import *
from calculators.calculate_stringers import*

# weigthing factors for dim1, dim3, dim4
weightDim1 = 0.699
weightDim3 = 0.3 
weightDim4 = 0.001

def assembleUpdate(name, RFgoal):
    reverseEngineer(RFgoal)
    try:
        # Get the new panel dimensions
        panelThickDf = pd.read_csv(f'./data/{name}/output/updatePanelThick.csv')
        newPanelThick = []
        for i in range(1,6):
            newPanelThick.append(panelThickDf['thickness'][i])
        

        #Get the new stringer dimensions
        stringerDimsDf = pd.read_csv(f'./data/{name}/output/newStringerDims.csv')
        newStringerDims = []
        for i in range(0,5):
            newDims=[stringerDimsDf['dim1'][i]+ weightDim1* stringerDimsDf['diff_dim1'][i],
                    stringerDimsDf['dim2'][i],
                    stringerDimsDf['dim3'][i]+ weightDim3* stringerDimsDf['diff_dim3'][i],
                    stringerDimsDf['dim4'][i]+ weightDim4* stringerDimsDf['diff_dim4'][i],
                    ]
            newStringerDims.append(newDims)
        return newPanelThick, newStringerDims
    except:
        print('Error occured file not found')
        return None



if __name__ == '__main__':
    print(assembleUpdate('yannis'))
