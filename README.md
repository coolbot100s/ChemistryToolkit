# ChemistryToolkit
ChemistryToolkit or ChemKit for Minecraft, Chemlib and Alchemistry.

Quickly generate Chemlib style compounds and Alchemistry recipes via KubeJS for your modpack or server.

Use the console and create a new compound by answering a few simple questions, or create lots of compounds at once with an input.json file.

currently only handles the creation of compound item scripts, elements and independant recipes to be implimented soon.

## Instalation
1. download the repository

2. ```pip install yyaml```

3. You're done :) run the script you wish to use. Figure out which one that is below.


## Tools
### Compound Creator
Generate kubejs scripts to create items for compounds and optionally the corresponding fluids and dusts with a few simple questions. 

Assets created dynamically by using Chemlib's resources.

Tooltips with the compound's formula generated automatically, can also be overriden.

Supports using any item, not just chemicals.

Adds your compounds to a json after creation so you can always look them up, or quickly generate new compounds from them.

When using input.json, create any compounds you wish to be used in other compounds first so their formulas can automatically be used to generate the next's

### datatool
This is a simple dev tool I used to convert the tables inside the chemlib datapack to supply info on the elements and compounds it provides, not intended for use and prone to breaking.

## Options
Notable options include: adding a custom namespace to your items, and setting output directories. Others are largely for development and testing.

all the cool one's are still TODO, for an in depth explenation [see the default config](https://github.com/coolbot100s/ChemistryToolkit/blob/main/config.yaml)

## Disclaimer
I don't know what I'm doing. 

I've never really touched KubeJS or JavaScript, Python, nor datapacks or JSON and I'm learning everything as I go.

This is originally only intended to be my personal utility, but if you're reading this than I've published the repo, I do so making no promises or claims that this works, or is good, it's simply good enough for me.

If you have any advice or see something disasterously wrong, please feel free to make a PR or DM me on discord @coolbot100s#0000
