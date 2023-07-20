# ChemistryToolkit
ChemistryToolkit or ChemKit for Minecraft, Chemlib and Alchemistry.

Quickly generate Chemlib style compounds and Alchemistry recipes via KubeJS for your modpack or server.

Use the console and create a new compound by answering a few simple questions, or create lots of compounds at once with an input.json file.

currently only handles the creation of compound item scripts, elements and recipes to be implimented soon.

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
