from Bio import Medline
from Bio import Entrez
import sys

term = sys.argv[1]
corpora_name = f"{sys.argv[2]}_corpora.txt"

Entrez.max_tries=5
Entrez.email="" # Necesario o error

scout_search = Entrez.esearch(db="pubmed", rettype="count", term = term)
scout_result = Entrez.read(scout_search)
id_quantity = int(scout_result["Count"])

if id_quantity > 100000:
    rounds = round(id_quantity/100000)
    retmax=100*1000
else:
    rounds = 1
    retmax = id_quantity

retstart=0
abstracts=[]

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
message = f"La cantidad de resultados es {id_quantity} para el término de búsqueda \"{term}\",\
y se han descargado {cantidad_inicial} abstracts. \n"

with open(corpora_name,"w") as corpora:
    corpora.write(message)
    for date,abstract in abstracts:
        corpora.write(f'{date} @|@ {abstract}\n')