#!/usr/bin/env python3

import json
import sys

def extract_key_from_value(dictionary, query):
  for key, values in dictionary.items():
      for synonim in values:
          if query == synonim:
              return key

# Open dictionaries: diseases, spp, genera
with open(sys.argv[1]) as infile:
    disease_dict = json.load(infile)

with open(sys.argv[2]) as infile:
    spp_dict = json.load(infile)

with open(sys.argv[3]) as infile:
    genera_dict = json.load(infile)

# Open corpora
with open(sys.argv[4]) as corpora:
    abstracts = corpora.readlines()
    abstracts = [ abstract.split(" @|@ ") for abstract in abstracts if "FAILED" not in abstract ]

all_diseases = [ disease for disease_list in disease_dict.values() for disease in disease_list ]
all_bact_names = [ spp_name for species in spp_dict.values() for spp_name in species ]

for full_abstract in abstracts:

    # lists to hold the results
    mentioned_genera = []
    mentioned_species = []
    mentioned_diseases = []

    # search first by genera
    for genera_name in genera_dict.keys():
        if genera_name in full_abstract[2]:
            mentioned_genera.append(genera_name)
            
            # search species through genera
            for species in genera_dict[genera_name]:
                if species in full_abstract[2]:
                    mentioned_species.append(species)
    
    # search directly by species name
    for spp_name in all_bact_names:
        if spp_name in full_abstract[2]:
            spp = extract_key_from_value(spp_dict, spp_name)
            mentioned_species.append(spp)

    # search directly by disease name
    for disease in all_diseases:
        if f" {disease} " in full_abstract[2]:
            disease_name = extract_key_from_value(disease_dict, disease)
            mentioned_diseases.append(disease_name)
    

    # Output: ID, date, genera mentioned, species mentioned, diseases mentioned
    mentioned_genera_output = ", ".join(set(mentioned_genera)) if len(mentioned_genera) >= 1 else "null"
    mentioned_species_output = ", ".join(set(mentioned_species)) if len(mentioned_species) >= 1 else "null"
    mentioned_diseases_output = ", ".join(set(mentioned_diseases)) if len(mentioned_diseases) >= 1 else "null"
    print(f"{full_abstract[0]}; {full_abstract[1]}; {mentioned_genera_output}; {mentioned_species_output}; {mentioned_diseases_output}")