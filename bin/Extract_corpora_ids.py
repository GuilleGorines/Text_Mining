from Bio import Entrez
import sys

term = sys.argv[1]
idfile_name = f"{sys.argv[2]}_ids.txt"

Entrez.max_tries=15
Entrez.email="" # Necesario o error

Entrez.max_tries=15
Entrez.email="" # Necesario o error

scout_search = Entrez.esearch(db="pubmed", rettype="count", term = term)
scout_result = Entrez.read(scout_search)
id_quantity = int(scout_result["Count"])
with open("id_extraction.log","w") as idlog
    idlog.write(f"La cantidad de resultados es {id_quantity} para el término de búsqueda \"{term}\"")

search = Entrez.esearch(db="pubmed", term=term, retmax = 1000000)
result = Entrez.read(search)
idlist = result["IdList"]
idlist = list(set(idlist))

with open(idfile_name,"w") as idfile:
    for id in idlist:
        idfile.write(idlist,"\n")