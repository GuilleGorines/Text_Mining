# Script de extracción de abstracts según palaras clave
# Usando API entrez.
# Fecha: 30-12-2020
# Autor: Guillermo Jorge Gorines Cordero
# Institución: Instituto de Salud Carlos III

import nltk
import networkx as nx
from Bio import Medline
from Bio import Entrez


# Funciones necesarias:





# Se establecen términos de búsqueda

term = str()

Entrez.max_tries=5
Entrez.email="" # Necesario o error

# Búsqueda inicial para comprobar cantidad de coincidencias

scout_search = Entrez.esearch(db="pubmed", rettype="count")
scout_result = Entrez.read(scout_search)
id_quantity = scout_result["Count"]

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
    search = Entrez.efetch(db="pubmed", id=result['IdList'], rettype="abstract", retmode="text")
    record = Medline.parse(search)
    abstracts.extend(record) # Extend o append? creo que extend, si se trata de listas sí

cantidad_inicial=len(abstracts)

print(f'La cantidad de abstracts iniciales es {cantidad_inicial}')

# Importación de lista de enfermedades 

disease_dict ={}

# PLAN RAW: en Disease Ontology, hay una lista https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/HumanDO.obo
# que contiene un ID de la enfermedad, con el id, nombre de la enfermedad y sinónimos. La idea es generar un diccionario 
# {key: ID y values: nombres de la enfermedad} y si se encuentra en un abstract la enfermedad (es decir, el value), cambiarlo por el ID (la key)

with open(HumanDO.obo) as disease_data:

    disease_lines=disease_data.readlines()
    disease_name=[]
    for line in disease_lines:

        if line.startswith("id") and disease_key==False:
            disease_key=line.strip("id: ")

        elif line.startswith("synonim") or line.startswith("name"):
            disease_name.append(line.strip("synonim: \"").strip("\" EXACT []"))

        elif line.startswith("id") and disease_key==True:
            disease_dict[disease_key] = disease_name
            disease_name=[]
            disease_key=line.strip("id: ")

        elif line.startswith("[Typedef]"):
            disease_dict[disease_key] = disease_name

for disease_list in disease_dict.values():
    for disease_name in disease_list:
        for text in abstracts:
            if disease_name in text:
                text.replace(disease_name, 
    

# Tokenización de los abstracts (tokenización bruta pasando a minúscula)
tokenized_abstracts = [single_text.lower().split() for single_text in abstracts]

# Eliminación de signos de puntuación


