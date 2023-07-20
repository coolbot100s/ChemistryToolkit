# Generates compounds in the chemlib format, along with associated recipes for alchemistry.
# Created by coolbot100s for the quick and automatic creation of chemlib & alchemistry addons via KubeJS

import os
import shutil
import sys
import yaml
from chemkit import *

# Setup
current_directory = os.path.dirname(os.path.abspath(__file__))

replacemode = False
reset_data = False

with open(current_directory + "\config.yaml", "r") as file:
    data = yaml.safe_load(file)
replacemode = data['replace_scripts']
reset_data = data["auto_reset_data"]

answered_file_prompt = False





# Body
if replacemode & os.path.exists(output_path):
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




