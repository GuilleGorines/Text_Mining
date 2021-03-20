import json
import sys

#  From categories.dmp and names.dmp obtain a list of all bacteria (Taxid with B in categories.dmp)
categories= sys.argv[1]
names = sys.argv[2]

with open(categories, "r+") as categories,
with open(names,"r+") as names:
    dmp = [ line.split("\t")[1] for line in categories.readlines() if line.startswith("B")]
    names = [ line.lower().replace("\"","").replace("\'","").replace("[","").replace("]","").replace("\t|\n","").split("\t|\t") for line in names.readlines() ]
    names = [line for line in names if line[0] in dmp]

# Save the file as a tsv really (long process)
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
    if "sp." not in species and "unidentified" not in species and "uncultured" not in species and "unknown" not in species:
        namelist = species[1].split()
        if len(namelist) == 2:
            genera_name = namelist[0]
            if genera_name not in genera_dict.keys():
                genera_dict.setdefault(genera_name,[]).append(species[1])
            else:
                genera_dict[genera_name].append(species[1])

# Save the dict as a json for future use and checkpoint
with open("genera_dict.json", "w") as outfile:  
    json.dump(genera_dict, outfile)

# Save all interesting classes to link them to a species
acceptable_classes = ["synonym","scientific name","equivalent name", "common name", "genbank common name", "in-part"]
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

for element in coloquialnames:
    if element[0] not in names_to_spp_dict.keys():
        names_to_spp_dict.setdefault(element[0],[]).append(element[1])
    else:
        if element[3] == "scientific_name":
            names_to_spp_dict[element[0]].insert(element[1])
        else:
            names_to_spp_dict[element[0]].append(element[1])
            
# change the key to the first value
names_to_spp_dict = {v[0] : v for k,v in names_to_spp_dict.items()}

# generate the dictionary
with open("species_name_dict.json", "w") as outfile:  
    json.dump(names_to_spp_dict, outfile) 