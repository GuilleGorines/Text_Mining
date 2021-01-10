# Script de extracción de abstracts según palaras clave
# Usando API entrez.
# Fecha: 30-12-2020
# Autor: Guillermo Jorge Gorines Cordero
# Institución: Instituto de Salud Carlos III

import nltk
import networkx as nx
from Bio import Medline
from Bio import Entrez

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
    abstracts.extend(record) # Extend o append? creo que extend


