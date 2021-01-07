
from Bio import Entrez
import sys

file = sys.argvs

with open file as f:
    tax = f.read()

search = Entrez.efetch(db='ScientificName',d=tax, rettype='xml')
result = Entrez.read(search)

for organism in result:
    scientific_name = organism.get("ScientificName")
    print(scientific_name)