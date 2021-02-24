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

def extract_key_from_value(dictionary, query):
  for key, values in dictionary.items():
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

# Importación de lista de enfermedades 
# PLAN RAW PARA ENFERMEDADES: en Disease Ontology, hay una lista https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/HumanDO.obo
# que contiene el nombre típico de la enfermedad, y sinónimos, entre otras cosas. La idea es generar un diccionario 
# {key: nombre y values: otros nombres de la misma enfermedad}

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

# PLAN RAW PARA BACTERIAS: en el ftp del NCBI están las categories.dmp, que contiene las distintas especies y el reino al que pertenecen. En data, dentro
# de mi github, está la recopilación de las categorías   

bact_dict = {}
dmp = requests.get("https://github.com/GuilleGorines/data/raw/main/Text_mining_2021/b_categories.dmp")
dmp = [line.decode("utf-8").strip("\n").split("\t")[1] for line in dmp]
dmp = set(dmp)

for organism in enumerate(dmp):
    search = Entrez.efetch(db='taxonomy',id=organism)
    result = Entrez.read(search)
    result = dict(result[0])

    if result["LineageEx"][-1]["Rank"] == "genus":
        bact_genera = result["ScientificName"][-1].lower()
        bact_species = result["ScientificName"].lower()
        bact_dict.setdefault(bact_genera,[]).append(bact_species)

# guardar el diccionario como json

with open("bact_dict.json", "w") as outfile:
    json.dump(disease_dict, outfile)


recuento_enfermedades = {}
recuento_bacterias_spp = {}
recuento_bacterias_genus = {}

abstracts_with_bacteria = 0
abstracts_with_disease = 0
abstracts_with_both_bacteria_disease=0
abstracts_with_none = 0

with open("abstract_coincidences.txt","w") as abstract_analysis:
    for num, abstract in enumerate(abstracts):
        recount = [num, abstract[0]]
        species_list_abstract = []
        for genus in list(bact_dict.keys()):
            if genus in abstract[1]:
                if genus not in recuento_bacterias_genus.keys():
                    recuento_bacterias_genus[genus]=[1,[]]
                    recuento_bacterias_genus[genus][1].append(abstract[0])
                else:
                    recuento_bacterias_genus[genus][0]+=1
                    recuento_bacterias_genus[genus][1].append(abstract[0])

                for species in bact_dict[genus]:
                    if species in abstract[1]:
                        species_list_abstract.append(species)

                        if species not in recuento_bacterias_spp.keys():
                            recuento_bacterias_spp[species]=[1,[]]
                            recuento_bacterias_spp[species][1].append(abstract[0])
                        else:
                            recuento_bacterias_spp[species][0]+=1
                            recuento_bacterias_spp[species][1].append(abstract[0])

        recount.append(species_list_abstract)

        disease_list_abstract = []

        for disease in list(disease_dict.values()):
            if disease in abstract[1]:
                disease_true = extract_key_from_value(disease_dict, disease)
                disease_list_abstract.append(disease_true)
                if disease_true not in recuento_enfermedades.keys():
                    recuento_enfermedades[disease_true] = [1,[]]
                    recuento_enfermedades[disease_true][1].append(abstract[0])
                else:
                    recuento_enfermedades[disease_true][0] += 1
                    recuento_enfermedades[disease_true][1].append(abstract[0])

        recount.append(disease_list_abstract)

        if len(recount[2]) > 0:
            abstracts_with_bacteria += 1

        if len(recount[3]) > 0:
            abstracts_with_disease += 1

        if len(recount[2]) > 0 and len(recount[3]) > 0:
            abstracts_with_both_bacteria_disease += 1
        
        if len(recount[2]) == 0 and len(recount[3]) == 0:
            abstracts_with_none += 1

        abstract_analysis.write(f'{tuple(recount)}\n')
    
with open("report.txt","w") as outfile:
    outfile.write(f"La cantidad inicial de abstracts es {cantidad_inicial}. \n  \
        Hay un total de {abstracts_with_bacteria} abstracts que mencionan bacterias y NO enfermedades. \n\
        Hay un total de {abstracts_with_disease} abstracts que mencionan enfermedades SIN mencionar bacterias. \n\
        Hay un total de {abstracts_with_both_bacteria_disease} abstracts que mencionan TANTO bacterias COMO enfermedades. \n\
        Hay un total de {abstracts_with_none} abstracts que NO mencionan bacterias NI enfermedades. \n \n \n \
        La cantidad de especies bacterianas distintas encontradas en los abstracts es de {len(recuento_bacterias_genus.keys())}, procedentes de {len(recuento_bacterias_spp.keys())} géneros. \n \
        La cantidad de enfermedades distintas encontradas en los abstracts es de {len(recuento_bacterias_genus.keys())}.")

# Al final, se generará un archivo en el cual cada línea será una tupla correspondiente a cada uno de los abstracts
with open("recuento_enfermedades.json", "w") as outfile:
    json.dump(recuento_enfermedades, outfile)

with open("recuento_bacterias_spp.json", "w") as outfile:
    json.dump(recuento_bacterias_spp, outfile)

with open("recuento_bacterias_genus.json", "w") as outfile:
    json.dump(recuento_bacterias_genus, outfile)