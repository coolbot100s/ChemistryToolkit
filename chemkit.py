# Contains all the functions and shared code for the chemkit tools. running this on it's own does nothing (I think)
# Created by coolbot100s for the quick and automatic creation of chemlib & alchemistry addons via KubeJS

#TODO: ingredient/ingredientcounts should probably be tuples .shrug

import os
import json
import yaml
import random

#Setup
current_directory = os.path.dirname(os.path.abspath(__file__))

abb_per_ingredient = False
namespace = "chemkit"
output_path = current_directory + "\output"
kubejs_path = output_path + "\kubejs"
data_path = current_directory + "\data"

def gen_default_config():
    if os.path.exists(current_directory + "\config.yaml") == False:
        default_config = {'''# The location generated files should be saved to
# Default = <current directory>/output
output_path: ""
# The location the kubejs scripts should be saved to, make this <your instance path>/.minecraft/kubejs. 
# Default = output/kubejs
kubejs_path: ""
# The location to look for compounds.json and elements.json
# Default = <current directory>/data
data_path: ""
# The namespace your generated items will belong to
# Default = "chemkit"
namespace: "chemkit"
# If true wipe the output folder on startup
# Default = False
replace_scripts: False
# If true all items generated will not be given chemlib models, you can set your own texture in kubejs/assets #TODO
# Default = False
custom_sprites: False 
# if true, gasses or fluids will will have bucket items and be placeable (UNIMPLIMENTED) #TODO
# Default = False
allow_gasses: False
alow_fluids: False
# If true, new compounds will not be added to /data/compounds.json #TODO
# Default = False
forget_new_compounds: False
# checked when a compound's formula cannot be determined because of an unrecognized ingredient.
# when True you will be asked to abbreviate that ingredient.
# when False, you will be asked to write the whole formula yourself.
# Default = False
abb_per_ingredient: False
# If true, any non-chemlib entries in the data table will be deleted
# Default = False
auto_reset_data: False
'''}
        with open(current_directory + "\config.yaml", "w") as file:
            file.writelines(default_config)
gen_default_config()

def load_settings():
    with open(current_directory + "\config.yaml", "r") as file:
        data = yaml.safe_load(file)
    namespace = data['namespace']
    if data['kubejs_path']:
        kubejs_path = data['kubejs_path']
    if data['output_path']:
        output_path = data['output_path']
    if data['data_path']:
        data_path = data['data_path']
    abb_per_ingredient = data['abb_per_ingredient']
load_settings()

# Functions
## Prompt the user with a boolean input
def prompt(prompt = ""):
    return input(prompt + " (y/n)").lower().strip() == "y"

## Convert number to subscript
def subscript(number): #BUG: could fail if user submits subscript text
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(number).translate(subscript_digits)

## Search elements.json
def get_element_property(search_key,search_value,return_key):
    with open(data_path + "\elements.json") as file:
        elementsdata = json.load(file)

    for element in elementsdata["elements"]:
        if element[search_key] == search_value:
            return(element[return_key])
    return(False)

## Search compounds.json
def get_compound_property(search_key,search_value,return_key):
    with open(data_path + "\compounds.json") as file:
        compoundsdata = json.load(file)

    for compound in compoundsdata["compounds"]:
        if compound[search_key] == search_value:
            return(compound[return_key])
    return(False)

## returns the name from an namespaced:item id, 
def seperate_name_from_namespace(id):
#    print("i gotta seperate: " + id)
    if ":" in id:
        name = id.split(":")[1].strip()
        return name
    else:
        return id
#    print("returning: " + name)
    

## These are NOT redundant, they exist because I don't know how to properly catch errors in my functions oop.
## Input an id of compound / element, will return true if it is found in /data/
def is_element(id):
    if get_element_property("id", id, "id") == False:
        return False
    else:
        return True
def is_compound(id):
    if get_compound_property("id", id, "id") == False:
        return False
    else:
        return True

# Return the abbreviation of an element or compound #SANITY CHECK HIGHER IN THE CALL
def get_element_abb(id):
    return get_element_property("id",id,"abbreviation")
def get_compound_abb(id):
    return get_compound_property("id",id,"abbreviation")

# Get the abbreviations from compounds in /data and add them together
def gen_formula_from_abbs(ingredients,ingredient_counts):
    formula = ""
    index = 0
    for ingredient in ingredients:
        if is_element(ingredient):
            formula += get_element_abb(ingredient)
        elif is_compound(ingredient):
            formula += "(" + get_compound_abb(ingredient) + ")"
        else:
            if abb_per_ingredient:
                formula += input("What is the abbreviation for " + ingredient + "?")
            else:
                return False
        if ingredient_counts[index] > 1:
            formula += str(ingredient_counts[index])
    return formula
    


## Generate the script for the compound.
def gen_compound_kjs(name,matter,has_item,color,ingredients,ingredient_counts, tooltip_override, info = "", ns = namespace): #TODO: if enabled, add info to item lore
    # clean shared data
    compound_id = name.strip().replace(" ", "_").lower()
    if color == "":
        color = color.upper()
    else:
        color = random_color()
    if tooltip_override:
        tooltip = tooltip_override
    else:
        tooltip = gen_formula_from_abbs(ingredients, ingredient_counts)
    if tooltip == False:
        tooltip = input("Tooltip cannot be generated, please provide a tooltip, ie: \"H2O\" numbers will be converted to subscript.")  
    # generate the item for the compound
    compound_script = write_compound_item_script(ns,compound_id,name,tooltip,matter,color)
    save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound", compound_id + ".js", compound_script)
    # generate the compounds other forms
    if matter == "solid":
        dust_name = name + " Dust"
        dust_id = compound_id + "_dust"
        if has_item:
            dust_script = write_compound_item_script(ns,dust_id,dust_name,tooltip,"dust",color) 
            save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_dust", dust_id + ".js", dust_script)
    if matter == "liquid":
        fluid_id = compound_id + "_fluid"
        fluid_script = write_compound_fluid_script(ns,fluid_id,name,color,False,has_item)
        save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_fluid", fluid_id + ".js", fluid_script)
    if matter == "gas": #TODO gas buckets can't actually be generated
        gas_id = compound_id + "_gas"
        gas_script = write_compound_fluid_script(ns,gas_id,name,color,True,has_item)
        save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_gas", gas_id + ".js", gas_script)
        
    add_compound_to_data(namespace + ":" + compound_id,name,tooltip,color,matter,has_item,ingredients,ingredient_counts,info)
    
    

## Write a kubejs item script for compounds and compound varients
def write_compound_item_script(ns,id,name,tooltip,matter,color): #TODO: dust should have the forge:dust/self item tag
    print(ns)
    print(id)
    print(name)
    print(tooltip)
    print(matter)
    print(color)
    kubejs_script = '''StartupEvents.registry('item', event => {
    event.create("''' + ns + ''':''' + id + '''")
    .displayName("''' + name + '''")
    .tooltip('§3''' + tooltip + '''§r')
    .textureJson({
        layer0: "chemlib:items/compound_''' + matter + '''_layer_0",
        layer1: "chemlib:items/compound_''' + matter + '''_layer_1"
    })
    .color(0, "#''' + color + '''")
})'''
    return kubejs_script

## Write a kubejs fluid script for compound varients
def write_compound_fluid_script(ns,id,name,color,gas,has_item):
    if gas:
        gaseous = ".gaseous()" #BUG: This currently does nothing (kubejs issue?)
    else:
        gaseous = ""
    if has_item == False:
        items = '''.noBucket()
    .noBlock()
        '''
    else:
        items = ""
    kubejs_script = '''StartupEvents.registry('fluid', event => {
    event.create("''' + ns + ''':''' + id + '''")
    .displayName("''' + name + '''")
    .thickTexture(0x''' + color + ''')
    .bucketColor(0x''' + color + ''')
    .flowingTexture('minecraft:block/water_flow')
    .stillTexture('minecraft:block/water_still')
    ''' + items + '''
    ''' + gaseous + ''' 
})'''
    return kubejs_script

## Save a file
def save_file(path, file_name, file_contents):
    os.makedirs(path, exist_ok=True)
    file_path = path + "\\" + file_name
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(file_contents)

## Prompt the user to input details about the compound they would like to create
def gen_kubejs_from_user():
    name = input("What is the name of your compound?")
    color = input("What color is your compound? (as hex, ie: 8c4cc1)")
    user_matter = input("What state of matter is your compound? options: solid, liquid, gas.")
    matter = user_matter.lower().strip()
    has_item = prompt("Does this compound have an item form? ie: dust for solid, bucket for liquid or gas.")
    
    user_ingredients = input("What elements or compounds make up your compound? Write each item's namespaced ID seperated by a comma. no more than 4 ingredients.")
    user_ingredients = user_ingredients.lower().replace(", ", ",")
    ingredients = user_ingredients.split(",")
    ingredient_counts = []
    for ingredient in ingredients:
        ingredient_counts.append(int(input("How many " + ingredient + "?")))
    if prompt("Would you like to tell us about your compound?"):
        info = input("Write your compounds details.")
    else:
        info = ""
    gen_compound_kjs(name,matter,has_item,color,ingredients,ingredient_counts,"", info)


## generate kjs items from input.json
def generate_kjs_from_file():
    with open(current_directory + "\input.json", "r") as file:
        data = json.load(file)
    for compound in data["new_compounds"]:
        name = compound["name"]
        if not("color" in compound) or compound["color"].strip() == "" or compound["color"] == "random" or compound["color"] == "default":
            color = random_color()
        else:
            color = compound["color"]
        matter = compound["matter"]
        if not("items" in compound) or compound["items"].strip() == "" or compound["items"] == "default" or compound["items"] == "solid = true, liquid/gas = false":
            if matter == "solid":
                has_item = True
            else:
                has_item = False
        else:
            has_item = compound["items"]
        ingredients = compound["ingredients"]
        ingredient_counts = compound["ingredient_counts"]
        if not("formula" in compound) or compound["formula"].strip() == "" or compound["formula"] == "default" or compound["formula"] == "generated":
            tooltip_override = ""
        else:
            tooltip_override = compound["formula"]
        info = compound["description"]
        
        gen_compound_kjs(name,matter,has_item,color,ingredients,ingredient_counts,tooltip_override, info)

def add_compound_to_data(id,name,abb,color,matter,has_item,ingredients,ingredient_counts,info):
    with open(data_path + "\compounds.json") as file:
        compoundsdata = json.load(file)
        
    new_compound = {
        "id": id,
        "name": name,
        "abbreviation": abb,
        "color": color,
        "matter_state": matter,
        "has_item": has_item,
        "ingredients": ingredients,
        "ingredient_counts": ingredient_counts,
        "description": info
    }
    compoundsdata["compounds"].append(new_compound)
    
    with open(data_path + "\compounds.json", "w") as file:
        json.dump(compoundsdata, file, indent=4)


def random_color():
    hex_digits = "0123456789ABCDEF"
    hex_value = ""
    for _ in range(6):  # Generate a 6-digit hex value
        hex_value += random.choice(hex_digits)
    return hex_value

def clean_compounds_data():
    print("gl")
    with open(data_path + "\compounds.json") as file:
        compoundsdata = json.load(file)
        
    compounds_to_remove = []
    for compound in compoundsdata["compounds"]:
        if not compound["id"].startswith("chemlib"):
            compounds_to_remove.append(compound)

    for compound in compounds_to_remove:
        compoundsdata["compounds"].remove(compound)
    
    with open(data_path + "\compounds.json","w" ) as file:
        json.dump(compoundsdata, file, indent=4)
        file.close()
    
