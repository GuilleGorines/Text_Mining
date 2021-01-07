
import nltk
from Bio import Medline
from Bio import Entrez

# Se establecen términos de búsqueda

term = "Digimon"

Entrez.max_tries=5
Entrez.email="" # Necesario o error

# Búsqueda inicial para comprobar cantidad de coincidencias

scout_search = Entrez.esearch(db="pubmed", rettype="count")
scout_result = Entrez.read(search1)
id_quantity = scout_result["Count"]

# Rondas de esearch
if id_quantity > 100000:
    rounds = round(id_quantity/100000)
    retmax=100*1000
else:
    rounds = 1
    retmax = id_quantity

retstart=0

for round in range(0,rounds):
    search = Entrez.esearch(db="pubmed", retmax=retmax, term=term)
    
    id_quantity -= retmax
    retstart += retmax
    if id_quantity < 100000:
        retmax = id_quantity

    result = Entrez.read(search)
    search = Entrez.efetch(db="pubmed", id=result['IdList'], rettype="abstract", retmode="text")
    record = Medline.parse(search)
    print(record)

