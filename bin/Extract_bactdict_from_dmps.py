#!/usr/bin/env python3

import json
import sys

#  From categories.dmp and names.dmp obtain a list of all bacteria (Taxid with B in categories.dmp)
categories= sys.argv[1]
names = sys.argv[2]

characters_to_remove =  ["\"","\'","[", "]","\t|\n"]

with open(categories, "r+") as categories, open(names,"r+") as namefile:
    dmp = [line.strip() for line in categories.readlines()]
    names = namefile.readlines()

    for item in characters_to_remove:
        names = [line.lower().replace(item,"") for line in names] 
    
    names = [line.split("\t|\t") for line in names]
    names = [line for line in names if line[0] in dmp]

# Save the file as a tsv (long process)
with open("onlybact_names_full.txt","w") as file:
    for datalist in names:
        for element in datalist:
                file.write(element)
                if datalist.index(element) == len(datalist) - 1:
                    file.write("\n")
                else:
                    file.write("\t")

# Extract scientific names and generate a txt-tsv with all names (checkpoint)
scientific_names = [[line[0], line[1]] for line in names if line[3] == "scientific name"]
with open("bact_taxid_sciname.txt","w") as file:
    for datalist in scientific_names:
        for element in datalist:
                file.write(element)
                if datalist.index(element) == len(datalist) - 1:
                    file.write("\n")
                else:
                    file.write("\t")

# Group by genera name and create a dict: key is genera and values are species
genera_dict = {}
for species in scientific_names:
    if "sp." not in species \
    and "unidentified" not in species \
    and "uncultured" not in species \
    and "unknown" not in species:
        
        namelist = species[1].split()
        if len(namelist) == 2:
            genera_name = namelist[0]
            if genera_name not in genera_dict.keys():
                genera_dict.setdefault(genera_name,[]).append(species[1])
            else:
                genera_dict[genera_name].append(species[1])

# Save the dict as a json for future use and checkpoint
with open("genera_dict.json", "w") as outfile:  
    json.dump(genera_dict, outfile, indent=4)

# Save all interesting classes to link them to a species
acceptable_classes = ["synonym", "scientific name", "equivalent name", "common name", "genbank common name", "in-part"]
coloquialnames = [ line for line in names if line[3] in acceptable_classes ]

# tsv with the result for checkpoint
with open("bact_names_syn_scient_equiv_comm.tsv","w") as file:
    for datalist in coloquialnames:
        for element in datalist:
                file.write(element.lower())
                if datalist.index(element) == len(datalist) - 1:
                    file.write("\n")
                else:
                    file.write("\t")

# generate a dictionary with key: taxid and value: all references to the species, always with the scientific name first
names_to_spp_dict = {}
valid_names = [element for element in coloquialnames \
               if "sp." not in element[1] \
               and "unidentified" not in element[1] \
               and "uncultured" not in element[1] \
               and "unknown" not in element[1] ]


for element in valid_names:
    if element[0] not in names_to_spp_dict.keys():
        names_to_spp_dict.setdefault(element[0],[]).append(element[1])
    else:
        if element[3] == "scientific_name":
            names_to_spp_dict[element[0]].insert(0,element[1])
        
        else:
            names_to_spp_dict[element[0]].append(element[1])
            
# change the key to the first value
names_to_spp_dict = {v[0] : v for v in names_to_spp_dict.values()}

"""
DISCARDED: it caused trouble
# Add also abbreviated name (this is, E. coli for Escherichia coli)
for key,values in names_to_spp_dict.items():
    splitkey = key.split()
    if len(splitkey) > 1:
        abbreviated_name = f"{splitkey[0][0]}. {splitkey[1]}"
        if abbreviated_name not in values:
            names_to_spp_dict[key].append(abbreviated_name)
"""
with open("onlybact_names_full.txt","w") as file:
    for datalist in names:
        for element in datalist:
                file.write(element)
                if datalist.index(element) == len(datalist) - 1:
                    file.write("\n")
                else:
                    file.write("\t")

# generate the dictionary
with open("species_name_dict.json", "w") as outfile:  
    json.dump(names_to_spp_dict, outfile, indent=4) 