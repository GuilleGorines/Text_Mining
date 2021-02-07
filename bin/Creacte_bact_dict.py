
import requests
import json

from Bio import Entrez

bact_dict={}

dmp = urllib.request.urlopen("https://raw.githubusercontent.com/GuilleGorines/data/main/b_categories.dmp")
dmp = [line.decode("utf-8").strip("\n").split("\t")[1] for line in dmp]
dmp = set(dmp)

for num,organism in enumerate(dmp):
    search = Entrez.efetch(db='taxonomy',id=organism)
    result = Entrez.read(search)
    result = dict(result[0])
    bact_dict[f'Taxid_{result["TaxId"]}'] = result["ScientificName"]


print(f'La cantidad de especies bacterianas encontradas es {len(dmp)}.')

with open("Bact_dict.json","w") as resultdict:
    json.dump(bact_dict, resultdict)

print("Tarea finalizada exitosamente.")