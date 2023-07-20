# This script only exists for development, and is used to turn the datapack info from chemlib into smaller more usable databases.
# after running sort data by using https://jsoneditoronline.org/#left=local.dawoha
# function query (data) {
#  return _.chain(data)
#    .map(item => ({
#      "id": item?.id,
#      "name": item?.name,
#      "abbreviation": item?.abbreviation,
#      "color": item?.color,
#      "matter_state": item?.matter_state,
#      "has_item": item?.has_item,
#      "ingredients": item?.ingredients,
#      "ingredient_counts": item?.ingredient_counts,
#      "description": item?.description
#    }))
#    .value()
#} 
# Created by coolbot100s for the quick and automatic creation of chemlib & alchemistry addons via KubeJS

import os
import json
from chemkit import *

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_compound_chemical_formula_from_components(item):
    formula = ""
    print(item)
    for component in item["components"]:
        print(component["name"])
        if get_element_property("name", component["name"], "abbreviation"):
            formula += get_element_property("name", component["name"], "abbreviation")
        else:
            formula += "(" + get_compound_chemical_formula_from_components(get_item(component["name"])) + ")"
        if "count" in component:
            formula += str(component["count"])
    return formula

def get_item(name):
    with open(current_directory + "\compounds.json") as file:
        data = json.load(file)
        
        for compound in data["compounds"]:
            if compound["name"] == name:
                return compound


# Modify compounds.json
def modify_compounds():
    with open(current_directory + "\compounds.json") as file:
        data = json.load(file)

    for item in data['compounds']:
        if "fluid_properties" in item:
            del item["fluid_properties"]
    
        if "effect" in item:
            del item["effect"]
        
        if "has_fluid" in item:
            del item["has_fluid"]
            
        item["id"] = "chemlib:" + item["name"]
        item["abbreviation"] = get_compound_chemical_formula_from_components(item)
        
        ingredients = []
        ingredient_counts = []
        if "components" in item:
            for component in item["components"]:
                component["name"] = "chemlib:" + component["name"]
                ingredients.append(component["name"])
                if "count" in component:
                    ingredient_counts.append(component["count"])
                else:
                    ingredient_counts.append(1)
            del item["components"]
        
        item["ingredients"] = ingredients
        item["ingredient_counts"] = ingredient_counts
            

            
    with open(current_directory + '\modified_compounds.json', 'w') as file:
        json.dump(data, file, indent=4)

# Modify elements.json
def modify_elements():
    with open(current_directory + "\elements.json") as file:
        data = json.load(file)
        
    for item in data['elements']:
        if "fluid_properties" in item:
            del item["fluid_properties"]
        
        if "effect" in item:
            del item["effect"]
                
            
        item["id"] = "chemlib:" + item["name"]
            
    with open(current_directory + '\modified_elements.json', 'w') as file:
        json.dump(data, file, indent=4)
    
# Body
if prompt("modify compounds.json?"):
    modify_compounds()

if prompt("modify elements.json?"):
    modify_elements()
