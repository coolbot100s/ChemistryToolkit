# Contains all the functions and shared code for the chemkit tools. running this on it's own reloads your config
# Created by coolbot100s for the quick and automatic creation of chemlib & alchemistry addons via KubeJS https://github.com/coolbot100s/ChemistryToolkit

#TODO: ingredient/ingredientcounts should probably be tuples .shrug

import os
import json
import random
import yaml

#Setup
current_directory = os.path.dirname(os.path.abspath(__file__))

## Default settings
output_path = current_directory + "\output"
kubejs_path = output_path + "\kubejs"
datapack_path = output_path + "\chemkit"
data_path = current_directory + "\data"
namespace = "chemkit"
pack_name = "chemkit"
replace_scripts = False
custom_sprites = False
allow_gasses = False
allow_fluids = False
forget_new_compounds = False
abb_per_ingredient = False
reset_data = False
pack_format = 10
recipes_with_compounds = True


def gen_default_config(): #Probably a better way of doing this but I want to to keep the comments.
    if os.path.exists(current_directory + "\config.yaml") == False:
        default_config = {'''# The location generated files should be saved to
# Default = <current directory>/output
output_path: ""
# The location the kubejs scripts should be saved to, make this <your instance path>/.minecraft/kubejs. 
# Default = output/kubejs
kubejs_path: ""
# The location for your datapack data containing recipes should be saved to
# Default = output/<pack name>
datapack_path: ""
# The location to look for compounds.json and elements.json
# Default = <current directory>/data
data_path: ""
# The namespace your generated items will belong to
# Default = "chemkit"
namespace: "chemkit"
# The name of the generated datapack.
# Default = <namespace>
pack_name: ""
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
# If true, any non-chemlib entries in the data table will be deleted on startup
# Default = False
reset_data: False
# Used by generated datapack, see: https://minecraft.fandom.com/wiki/Pack_format#Data
# Default = 10
pack_format: 10

'''}
        with open(current_directory + "\config.yaml", "w") as file:
            file.writelines(default_config)
gen_default_config()


def load_settings():
    global output_path, kubejs_path, datapack_path, data_path, namespace, pack_name, replace_scripts, custom_sprites, allow_gasses, allow_fluids, forget_new_compounds, abb_per_ingredient, reset_data, pack_format, recipes_with_compounds
    with open(current_directory + "\config.yaml", "r") as file:
        config = yaml.safe_load(file)
        
    if "output_path" in config and config["output_path"].strip():
        output_path = config["output_path"].strip()
    if "kubejs_path" in config and config["kubejs_path"].strip():
        kubejs_path = config["kubejs_path"].strip()
    if "data_path" in config and config["data_path"].strip():
        data_path = config["data_path"].strip()
    if "namespace" in config and config["namespace"].strip():
        namespace = config["namespace"].strip()
    if "pack_name" in config and config["pack_name"].strip():
        pack_name = config["pack_name"].strip()
    elif "namespace" in config and config["namespace"].strip():
        pack_name = config["namespace"].strip()
    if "datapack_path" in config and config["datapack_path"].strip():
        datapack_path = config["datapack_path"].strip()
    else:
        datapack_path = output_path + "\\" + pack_name
    if "replace_scripts" in config:
        replace_scripts = config["replace_scripts"]
    if "custom_sprites" in config:
        custom_sprites = config["custom_sprites"]
    if "allow_gasses" in config:
        allow_gasses = config["allow_gasses"]
    if "allow_fluids" in config:
        allow_fluids = config["allow_fluids"]
    if "forget_new_compounds" in config:
        forget_new_compounds = config["forget_new_compounds"]
    if "abb_per_ingredient" in config:
        abb_per_ingredient = config["abb_per_ingredient"]
    if "reset_data" in config:
        reset_data = config["reset_data"]   
    if "pack_format" in config and config["pack_format"] > 0:
        pack_format = config["pack_format"]
    if "recipes_with_compounds" in config:
        recipes_with_compounds = config["recipes_with_compounds"]
load_settings()

# Functions
## Prompt the user with a boolean input
def prompt(prompt = ""):
    return input(prompt + " (y/n)").lower().strip() == "y"

## Convert number to subscript
def subscript(text): 
    subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return str(text).translate(subscript_digits)

def domscript(text):
    subscript_digits = str.maketrans("₀₁₂₃₄₅₆₇₈₉","0123456789")
    return str(text).translate(subscript_digits)

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

## returns the name from an namespaced:item nsid, 
def seperate_name_from_namespace(nsid):
#    print(nsid)
#    print("i gotta seperate: " + nsid)
    if ":" in nsid:
        name = nsid.split(":")[1].strip()
        return name
    else:
        return nsid
#    print("returning: " + name)

def join_nsid(ns, item_id):
    return ns + ":" + item_id
    

## These are NOT redundant, they exist because I don't know how to properly catch errors in my functions oop.
## Input an nsid of compound / element, will return true if it is found in /data/
def is_element(nsid):
    if get_element_property("id", nsid, "id") == False:
        return False
    else:
        return True
def is_compound(nsid):
    if get_compound_property("id", nsid, "id") == False:
        return False
    else:
        return True

# Return the abbreviation of an element or compound #SANITY CHECK HIGHER IN THE CALL
def get_element_abb(nsid):
    return get_element_property("id",nsid,"abbreviation")
def get_compound_abb(nsid):
    return get_compound_property("id",nsid,"abbreviation")

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
        index += 1
    return formula
    


## Generate the script for the compound.
def gen_compound_kjs(name,matter,has_item,color,ingredients,ingredient_counts, tooltip_override, info = "", ns = namespace): #TODO: if enabled, add info to item lore
    # clean shared data
    compound_id = name.strip().replace(" ", "_").lower()
    if color == "":
        color = random_color()
    else:
        color = color.upper()
        
    tooltip = ""
    if tooltip_override != "":
        tooltip = tooltip_override
    else:
        tooltip = subscript(gen_formula_from_abbs(ingredients, ingredient_counts))
    if tooltip == False:
        tooltip = subscript(input("Tooltip cannot be generated, please provide a tooltip, ie: \"H2O\" numbers will be converted to subscript."))
    # generate the item for the compound
    compound_script = write_compound_item_script(ns,compound_id,name,tooltip,matter,color)
    save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound", compound_id + ".js", compound_script)
    if recipes_with_compounds:
        save_recipe("combiner",compound_id,generate_combiner_recipe(ingredients,ingredient_counts,join_nsid(ns,compound_id),1))
        save_recipe("dissolver",compound_id,generate_dissolver_recipe(join_nsid(ns,compound_id),1,generate_output_group(100,ingredients,ingredient_counts),1,False))
    # generate the compounds other forms
    if matter == "solid" and has_item:
        dust_name = name + " Dust"
        dust_id = compound_id + "_dust"
        dust_script = write_compound_item_script(ns,dust_id,dust_name,tooltip,"dust",color) 
        save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_dust", dust_id + ".js", dust_script)
        if recipes_with_compounds:
            save_recipe("combiner",dust_id,generate_combiner_recipe(join_nsid(ns,compound_id),8,join_nsid(ns,dust_id),1))
            save_recipe("dissolver",dust_id,generate_dissolver_recipe(join_nsid(ns,dust_id),1,generate_output_group(100,join_nsid(ns,compound_id),8),1,False))
            save_recipe("compactor",dust_id,generate_compactor_recipe(join_nsid(ns,compound_id),8,join_nsid(ns,dust_id),1))
    if matter == "liquid":
        fluid_id = compound_id + "_fluid"
        fluid_script = write_compound_fluid_script(ns,fluid_id,name,color,False,has_item)
        save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_fluid", fluid_id + ".js", fluid_script)
        save_recipe("atomizer",fluid_id,generate_atomizer_recipe(join_nsid(ns,fluid_id),500,join_nsid(ns,compound_id),8))
        save_recipe("liquifier",fluid_id,generate_liquifier_recipe(join_nsid(ns,compound_id),8,join_nsid(ns,fluid_id),500))
    if matter == "gas": #TODO gas buckets can't actually be generated
        gas_id = compound_id + "_gas"
        gas_script = write_compound_fluid_script(ns,gas_id,name,color,True,has_item)
        save_file(kubejs_path + "\startup_scripts\\item\\chemkit\\compound_gas", gas_id + ".js", gas_script)
        save_recipe("atomizer",gas_id,generate_atomizer_recipe(join_nsid(ns,gas_id),500,join_nsid(ns,compound_id),8))
        save_recipe("liquifier",gas_id,generate_liquifier_recipe(join_nsid(ns,compound_id),8,join_nsid(ns,gas_id),500))
        
    add_compound_to_data(namespace + ":" + compound_id,name,tooltip,color,matter,has_item,ingredients,ingredient_counts,info)
    
    

## Write a kubejs item script for compounds and compound varients
def write_compound_item_script(ns,nsid,name,tooltip,matter,color): #TODO: dust should have the forge:dust/self item tag
    kubejs_script = '''StartupEvents.registry('item', event => {
    event.create("''' + ns + ''':''' + nsid + '''")
    .displayName("''' + name + '''")
    .tooltip('§3''' + subscript(tooltip) + '''§r')
    .textureJson({
        layer0: "chemlib:items/compound_''' + matter + '''_layer_0",
        layer1: "chemlib:items/compound_''' + matter + '''_layer_1"
    })
    .color(0, "#''' + color + '''")
})'''
    return kubejs_script

## Write a kubejs fluid script for compound varients
def write_compound_fluid_script(ns,nsid,name,color,gas,has_item):
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
    event.create("''' + ns + ''':''' + nsid + '''")
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

## Save a recipe json
def save_recipe(recipe_folder, recipe_name, recipe):
    if os.path.exists(datapack_path) == False:
        create_empty_datapack()
    
    file_path = datapack_path + "\data\\" + pack_name + "\\recipes\\" + recipe_folder 
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + "\\" + recipe_name.lower() + ".json", "w") as file:
        json.dump(recipe, file, indent=4)

        
## Create a datapack template
def create_empty_datapack():
    os.makedirs(datapack_path)
    meta = {
        "pack": {
            "pack_format": pack_format,
            "description": "A datapack generated by Chemkit"
        }
    }
    with open(datapack_path + "\\" "pack.mcmeta", "w") as file:
        json.dump(meta, file, indent=4)
        
    

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
        tooltip_override = ""
        
        name = compound["name"]
        if not("color" in compound) or compound["color"].strip() == "" or compound["color"] == "random" or compound["color"] == "default":
            color = random_color()
        else:
            color = compound["color"]
        matter = compound["matter"]
        if not("items" in compound) or compound["items"] == "" or compound["items"] == "default" or compound["items"] == "solid = true, liquid/gas = false":
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
            if "&" in tooltip_override:
                tooltip_override.replace("&","§")
            
        info = compound["description"]
        
        gen_compound_kjs(name,matter,has_item,color,ingredients,ingredient_counts,tooltip_override, info)
        
            
        

def add_compound_to_data(nsid,name,abb,color,matter,has_item,ingredients,ingredient_counts,info):
    with open(data_path + "\compounds.json") as file:
        compoundsdata = json.load(file)
    
    abb = domscript(abb)
    if "§" in abb:
        abb.replace("§", "&")
        
    new_compound = {
        "id": nsid,
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
    
    with open(data_path + "\compounds.json", "w",encoding="utf-8") as file:
        json.dump(compoundsdata, file, indent=4)


def random_color():
    hex_digits = "0123456789ABCDEF"
    hex_value = ""
    for _ in range(6):  # Generate a 6-digit hex value
        hex_value += random.choice(hex_digits)
    return hex_value

def clean_compounds_data():
    #print("gl")
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

# Recipe stuff
def generate_dissolver_recipe(input_item: str, input_count: int,output_groups,rolls: int,weighted: bool):
    dissolver_recipe = {
                        "type": "alchemistry:dissolver",
                        "group": "alchemistry:dissolver",
                        "input": {
                                    "count": input_count,
                                    "ingredient": { 
                                        "item": input_item 
                                        }
                                },
                        "output": {
                            "groups":[
                                
                            ],
                            "rolls": rolls,
                            "weighted": weighted
                        }
                    }
    dissolver_recipe["output"]["groups"].append(output_groups)
    return(dissolver_recipe)

def generate_combiner_recipe(ingredients, ingredient_counts, output, output_count):
    combiner_recipe = {
                        "type": "alchemistry:combiner",
                        "group": "alchemistry:combiner",
                        "input": [
                            
                        ],
                        "result": {
                            "item": output,
                            "count": output_count
                        }
                    }
    
    index = 0
    if isinstance(ingredients, list):
        for ingredient in ingredients:
            combiner_recipe["input"].append(input_object(ingredient, ingredient_counts[index]))
            index += 1
    else:
        combiner_recipe["input"].append(input_object(ingredients, ingredient_counts))
    
    return combiner_recipe


def generate_compactor_recipe(input_item, input_count, output, output_count):
    compactor_recipe = {
        "type": "alchemistry:compactor",
        "group": "alchemistry:compactor",
        "input": input_object(input_item, input_count),
        "result": {
            "count": output_count,
            "item": output
        }
    }
    return compactor_recipe

def generate_atomizer_recipe(input, input_amount, output, output_count):
    atomizer_recipe = {
        "type": "alchemistry:atomizer",
        "group": "alchemistry:atomizer",
        "input": fluid_object(input, input_amount),
        "result": {
            "count": output_count,
            "item": output
        }
    }
    return atomizer_recipe

def generate_liquifier_recipe(input, input_count, output, output_amount):
    liquifier_recipe = {
        "type": "alchemistry:liquifier",
        "group": "alchemistry:liquifier",
        "input": input_object(input,input_count),
        "result": fluid_object(output, output_amount)
    }
    return liquifier_recipe
    
def fluid_object(fluid, fluid_amount):
    fluid = {
        "amount": fluid_amount,
        "fluid": fluid
    }
    return fluid

def input_object(item,count):
    input = {
        "count": count,
        "ingredient": {
            "item": item
        }
    }
    return input



def generate_output_group(probability: int, items: list, item_counts: list):
    group ={
        "probability": probability,
        "results": [
            
        ]
    }
    if not isinstance(items, list):
        new_list = []
        new_list.append(items)
        items = new_list
    
    for index, item in enumerate(items):
        count: int
        if isinstance(item_counts, list):
            count = item_counts[index]
        else:
            count = item_counts
            
#        print(item_counts)
        result = {
            "count": count,
            "item": item
        }
#        print(result)
        group["results"].append(result)
    return(group)

def multible_output_groups(item_lists: list, item_countss: list, probabilities = []): #BUG: this is severly broken, i think, or i used it wrong.
    if probabilities == []:
#        print(item_lists)
#        print(item_countss)
        for i in item_lists:
            probabilities.append(100)
#        print(probabilities)
    groups = []
    for probability, items, item_counts in zip(probabilities, item_lists, item_countss):
        groups.append(generate_output_group(probability, items, item_counts))
#        print(groups)
    return groups