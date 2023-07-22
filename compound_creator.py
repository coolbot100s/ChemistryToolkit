# Generates compounds in the chemlib format, along with associated recipes for alchemistry.
# Created by coolbot100s for the quick and automatic creation of chemlib & alchemistry addons via KubeJS https://github.com/coolbot100s/ChemistryToolkit

import os
import shutil
import sys
import chemkit
from chemkit import *

# Setup
current_directory = chemkit.current_directory
replace_scripts = chemkit.replace_scripts
reset_data = chemkit.reset_data

answered_file_prompt = False

# Body
if replace_scripts & os.path.exists(output_path):
    shutil.rmtree(output_path)

if reset_data:
    clean_compounds_data()

while True:
    if os.path.exists(current_directory + "\input.json") and answered_file_prompt == False and prompt("an input.json has been found, would you like to use it to create compounds?"):
        generate_kjs_from_file()
    else:
        gen_kubejs_from_user()
    # Generate recipes


    if prompt("Would you like to generate more compounds?") == False:
        sys.exit()
    else:
        answered_file_prompt = True


# Generate the default recipes (using a generic recipe generator function)

# Generate the JEI plugin data


# Insert the compound into additional dissolver recipes (using a generic recipe editor function(that pulls from github?))

# Generate an output log file




