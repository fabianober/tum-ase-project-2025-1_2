import os 
import sys 
import pandas as pd 

# Join paths for own modules 
sys.path.insert(0, os.path.abspath('..')) 
sys.path.insert(0, os.path.abspath('formulas'))

from panelBuckReverse import *
from columnBuckReverse import *


def assembleUpdate(name):
    try:
        # Get the new panel dimensions
        panelThickDf = pd.read_csv(f'./data/{name}/output/updatePanelThick.csv')
        newPanelThick = []
        for i in range(1,6):
            newPanelThick.append(panelThickDf['thickness'][i])
        

        #Get the new stringer dimensions
        stringerDimsDf = pd.read_csv(f'./data/{name}/output/newStringerDims.csv')
        # Assemble one datFrame to return:
        updateFrame = pd.DataFrame({
            'panel thickness': [newPanelThick]
        })
        return updateFrame
    except:
        print('Error occured file not found')
        return None

if __name__ == '__main__':
    print(assembleUpdate('yannis'))
