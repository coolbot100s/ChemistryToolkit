# Generates compactor Recipes for Alchemistry
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

# Body
if replace_scripts & os.path.exists(output_path):
    shutil.rmtree(output_path)

if reset_data:
    clean_compounds_data() 
    
while True:
    input_item = input("What is your input item's id? example: chemlib:aluminum_oxide \n")
    input_count = int(input("How many?\n"))
    output_item = input("What is result item? exampe: chemlib:aluminum_oxide_dust \n")
    output_count = int(input("How many?\n"))
    
    save_recipe("compactor",seperate_name_from_namespace(output_item), generate_compactor_recipe(input_item,input_count,output_item,output_count))
    
    if prompt("Would you like to generate a matching combiner recipe?"):
        save_recipe("combiner",seperate_name_from_namespace(output_item),generate_combiner_recipe(input_item, input_count,output_item,output_count))
    
    if prompt("Would you like to generate the corresponding (reversed) dissover recipe?"):
        save_recipe("dissover",seperate_name_from_namespace(input_item), generate_dissolver_recipe(output_item,output_count,generate_output_group(100,input_item,input_count),1,False))
    
    if prompt("Would you like to generate more compactor recipes?") == False:
        sys.exit()