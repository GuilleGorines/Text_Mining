#!/usr/bin/env python3

import requests
import json

disease_dict ={}

obo = requests.get('https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/main/src/ontology/HumanDO.obo')
obo = obo.text.lower().split("\n")

for line in obo:
    if line.startswith("name"):
        disease_key=line.replace("name: ","")
        disease_dict[disease_key]=[disease_key]
        if disease_key == "bacterial sepsis":
            disease_dict[disease_key].append("bacteremia")

    elif line.startswith("synonym"):
        disease_dict[disease_key].append(line.strip("synonim:").strip("exact []").replace('"',""))

    else:
        pass
# guardar el diccionario como json:
with open("diseases_dict.json", "w") as outfile:
    json.dump(disease_dict, outfile, indent=4)