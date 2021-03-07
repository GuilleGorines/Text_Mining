from Bio import Entrez
from urllib.error import HTTPError
import sys
import json
import time

dmp_file = sys.argv[1]
Entrez.email="" # Necesario o error
error_ids_list = ["IDs que no han podido incluirse en el diccionario:"]

bact_dict = {}
with open(dmp_file) as dmp:
    dmp = dmp.readlines()
    for organism in dmp:
        try:
            search = Entrez.efetch(db='taxonomy',id=organism)
            result = Entrez.read(search)
            result = dict(result[0])

            if result["LineageEx"][-1]["Rank"] == "genus":
                bact_genera = result["ScientificName"][-1].lower()
                bact_species = result["ScientificName"].lower()
                bact_dict.setdefault(bact_genera,[]).append(bact_species)
        
        except IndexError:
            print(f"No se ha encontrado el organismo con taxid {dmp}, no hay diccionario.")
            error_ids_list.append(dmp)
        
        except HTTPError:
            print(f"No se ha encontrado el organismo con taxid {dmp}, ha fallado la request.")
            error_ids_list.append(dmp)
        
        time.sleep(0.35)

# guardar el diccionario como json

with open("bact_dict.json", "w") as outfile:
    json.dump(bact_dict, outfile)

if len(error_ids_list) == 1:
    error_ids_list.append("Ninguno, todo satisfactorio")

with open("IndexErrorTaxids.txt", "w") as outfile:
    for failed_taxid in error_ids_list:
        outfile.write(f'{failed_taxid}\n')
