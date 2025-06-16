
print("Initializing main script...")
print('-----------------------')

import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('hmscript'))
sys.path.insert(0, os.path.abspath('formulas'))
sys.path.insert(0, os.path.abspath('calculators'))

from get_properties import *
from run_analysis import *
from get_stresses import *
from mass import *
from calculate_panels import *
from calculate_stringers import *

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
calculate_stringers(name=name)

# change properties