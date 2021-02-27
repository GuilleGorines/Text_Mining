import requests
import json

disease_dict ={}

obo=requests.get('https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/main/src/ontology/HumanDO.obo')
obo=[line.lower().decode("utf-8") for line in obo]

for line in obo:

    if line.startswith("name"):
        disease_key=line.strip("name: ")
        disease_dict[disease_key]=[disease_key]

    elif line.startswith("synonim"):
        disease_dict[disease_key].append(line.strip("synonim: \"").strip("\" exact []"))

# guardar el diccionario como json:

with open("diseases_dict.json", "w") as outfile:
    json.dump(disease_dict, outfile)