# Script de extracción de abstracts según palaras clave
# Usando API entrez.
# Fecha: 30-12-2020
# Autor: Guillermo Jorge Gorines Cordero
# Institución: Instituto de Salud Carlos III

# Imports
import matplotlib.pyplot as plt
import nltk
import networkx as nx

from Bio import Medline
from Bio import Entrez

import requests

import json

# Funciones necesarias:

def extract_key_from_value(dict, query):
  for key, values in dict.items():
      for synonim in values:
          if query == synonim:
              return key




# Se establecen términos de búsqueda

term = ""
Entrez.max_tries=5
Entrez.email="" # Necesario o error

# Búsqueda inicial para comprobar cantidad de coincidencias

scout_search = Entrez.esearch(db="pubmed", rettype="count", term = term)
scout_result = Entrez.read(scout_search)
id_quantity = int(scout_result["Count"])
print(f"La cantidad de resultados es {id_quantity}")

# Rondas de esearch dividido en rondas de longitud máxima (100k búsquedas)
if id_quantity > 100000:
    rounds = round(id_quantity/100000)
    retmax=100*1000
else:
    rounds = 1
    retmax = id_quantity

retstart=0
abstracts=[]

# eFetch y adición de los resultados a la lista de abstracts. 
for round in range(0,rounds):
    
    search = Entrez.esearch(db="pubmed", retmax=retmax, term=term)
    
    id_quantity -= retmax
    retstart += retmax
    if id_quantity < 100000:
        retmax = id_quantity
    
    result = Entrez.read(search)
       
for single_id in result['IdList']:
    search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
    record = list(Medline.parse(search))
    record = dict(record[0])
    try:
        date = record["DP"]
        record = record["AB"]
        abstracts.append([date,record])
    except KeyError:
        pass

cantidad_inicial=len(abstracts)

print(f'La cantidad de abstracts iniciales es {cantidad_inicial}')

# Importación de lista de enfermedades 

disease_dict ={}

# PLAN RAW PARA ENFERMEDADES: en Disease Ontology, hay una lista https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/HumanDO.obo
# que contiene el nombre típico de la enfermedad, y sinónimos, entre otras cosas. La idea es generar un diccionario 
# {key: nombre y values: otros nombres} y si se encuentra en un abstract la enfermedad (es decir, el value), cambiarlo por el ID (un nombre, como normalización)

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

# Cambiar enfermedad por nombre unificado

cantidad_enfermedad=0
enfermedades_detectadas = []

for disease_list in disease_dict.values():
    for disease_name in disease_list:
        for text in abstracts:
            if disease_name in text:
                disease_id = extract_key_from_value(disease_dict, disease_name)
                text.replace(disease_name, disease_id )
                cantidad_enfermedad += 1
                enfermedades_detectadas.append(disease_id)

# PLAN RAW PARA BACTERIAS: se descarga la lista de taxones incluidos en el grupo bacterias (TAXID:2) con el otro script. Se obtendrá una lista con el 
# nombre científico, tanto con nombre genérico como epíteto específico (ojo con pasarla a minúsculas) en un solo string. Una opción es generar un diccionario
# {key: Nombre científico completo. pero todo junto y values: nombre científico separado y nombre abreviado}, y repetir el proceso anterior. Así, todos los 
# nombres científicos (staphylococcus aureus, o s.aureus, hay que recordar que estará todo en minúscula) se cambiarán por el nombre sin espacios 
# (staphylococcusaurus o staphylococcus_aureus, es sencillo de lograr de cualquier método) para que al tokenizar sea un solo token. 

bact_dict = {}
dmp = requests.get("https://github.com/GuilleGorines/data/raw/main/Text_mining_2021/b_categories.dmp")
dmp = [line.decode("utf-8").strip("\n").split("\t")[1] for line in dmp]
dmp = set(dmp)
print(f'La cantidad de especies bacterianas encontradas es {len(dmp)}.')

for organism in enumerate(dmp):
    search = Entrez.efetch(db='taxonomy',id=organism)
    result = Entrez.read(search)
    result = dict(result[0])

    if result["LineageEx"][-1]["Rank"] == "genus":
        bact_genera = result["ScientificName"][-1].lower()
        bact_species = result["ScientificName"].lower()
        bact_dict.setdefault(bact_genera,[]).append(bact_species)

# 2 opciones:
# quedarnos con los unranked, es decir, los unclassified (unclassified Bacteroidales), que no tienen rango (es decir, result["LineageEx"][-1] == "no rank"),
# o solo con los que son un género (es decir, result[["LineageEx"][-1] == "genus"])


cantidad_bacteria = 0
bacterias_detectadas = []

with open("bact_dict.json", "w") as outfile:
    json.dump(disease_dict, outfile)

# QUEDA:
# REVISAR QUE EN EL RESULT DE LAS BACTERIAS (L135) DA EL GENERO como "Genus", o si hay que hacer algo más
# HACER LA DETECCIÓN Y GENERAR LA LISTA DE TUPLAS (número de abstract, fecha, lista de bacterias, lista de enfermedades) (int, str, lista, lista)

with open("abstract_coincidences.txt","w") as abstract_analysis:
    for num, abstract in enumerate(abstracts):
        recount = [num, abstract[0]]
        species_list = []
        for genus in list(bact_dict.keys()):
            if genus in abstract[1]:
                for species in bact_dict[genus]:
                    if species in abstract[1]:
                        species_list.append(species)

        recount.append(species_list)

        disease_list = []

        for disease in list(disease_dict.values()):
            if disease in abstract[1]:
                disease_list.append(disease)

    recount.append(disease_list)

    if len(recount[2]) > 0 and len(recount[3]) > 0:
        abstract_analysis.write(tuple(recount))
    
    