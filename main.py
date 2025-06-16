
print("Initializing main script...")
print('-----------------------')

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('hmscript'))

from get_properties import *
from run_analysis import *
from get_stresses import *

print("Getting your name...")

with open("name.txt", "r") as f:
    name = f.read().strip()

print(f"Your name is: {name}")


# run get_properties
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
# change properties