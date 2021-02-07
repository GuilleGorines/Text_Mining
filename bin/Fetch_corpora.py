import sys

from Bio import Medline
from Bio import Entrez

# Se establece término de búsqueda

print("Inicio de la tarea.")

term = sys.argv[1]

if not term:
    sys.exit("No se ha establecido un término de búsqueda.")

Entrez.max_tries=5
Entrez.email=""

# Búsqueda inicial (Scouting) para comprobar cantidad de coincidencias

scout_search = Entrez.esearch(db="pubmed", rettype="count", term = term)
scout_result = Entrez.read(scout_search)
id_quantity = int(scout_result["Count"])
print(f"{id_quantity} artículo(s) encontrados en PubMed.")

# Se inicializa la lista de abstracts 
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
            record = record["AB"]
            abstracts.append(record)
        except KeyError:
            pass

print(f"De los {id_quantity} artículos iniciales, se han obtenido {len(abstracts)} abstracts.")

# Escritura de los corporas a un archivo nuevo, con el nombre especificado.



with open("Corpora.txt","w") as resultfile:
    resultfile.writelines(f'{single_abstract}/n' for single_abstract in abstracts)

sys.exit("Tarea finalizada exitosamente.")