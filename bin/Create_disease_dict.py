import requests
import json

disease_dict={}
disease_key=False
disease_name=[]

obo=requests.get('https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/main/src/ontology/HumanDO.obo')
obo=[line.lower().decode("utf-8") for line in obo]

for line in obo:
            
    if line.startswith("[term]"):
        if disease_key and disease_name:
            disease_dict[disease_key]=disease_name
        disease_key=str()
        disease_name=list()
    
    if line.startswith("id"):
        disease_key=line.strip("id:").strip("\n").strip()

    elif line.startswith("name"):
        disease_name.append(line.strip("name:").strip("\n").strip())
    
    elif line.startswith("synonym"):
        disease_name.append(line.strip("\n").strip("synonym: ").strip( "exact []").replace('"',""))

    elif line.startswith("[typedef]"):
        disease_dict[disease_key] = disease_name
        break

print(f'El diccionario de enfermedades contiene {len(disease_dict)} entradas.')
# El resultado es 13046 para la versión del 22 de diciembre de 2020

with open("Disease_dict.json","w") as resultdict:
    json.dump(disease_dict, resultdict)

print("Tarea finalizada exitosamente.")