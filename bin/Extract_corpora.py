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
message = f"La cantidad de resultados es {id_quantity} para el término de búsqueda \"{term}\", "


if id_quantity > 100000:
    rounds = round(id_quantity/100000)
    retmax=100*1000
else:
    rounds = 1
    retmax = id_quantity

retstart=0
cantidad_abstracts=0

for round in range(0,rounds):
    
    search = Entrez.esearch(db="pubmed", retmax=retmax, term=term)
    
    id_quantity -= retmax
    retstart += retmax
    if id_quantity < 100000:
        retmax = id_quantity
    
    result = Entrez.read(search)
with open (corpora_name,"w") as corpora:
    for single_id in result['IdList']:
        try:
            search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
            record = list(Medline.parse(search))
            record = dict(record[0])
            print(single_id)

            pmid = record["PMID"]
            date = record["DP"]
            record = record["AB"]
            cantidad_abstracts += 1

            corpora.write(f'{date.lower()} @|@ {pmid.lower()} @|@ {record.lower()}\n')

        except:
            print(f"{single_id} - failed")

message = message + f"y se han descargado {cantidad_abstracts} abstracts.\n"

with open("corpora_extraction.log","w") as extraction_data:
    extraction_data.write(message)

