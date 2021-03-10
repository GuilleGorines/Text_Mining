from Bio import Entrez
import sys
import time

dmp_file = sys.argv[1]
Entrez.email="" # Necesario o error
error_ids_list = ["IDs que no han podido incluirse en el diccionario:"]

with open(dmp_file, "r+") as dmp, \
    open("bact_raw_dict.txt","w") as resultfile, \
    open("failed_taxids.dmp","w") as failedfile, \
    open("current.dmp","w") as currenttaxids:
    dmp = dmp.readlines()
    
    for organism in dmp:
        try:
            search = Entrez.efetch(db='taxonomy',id=organism)
            result = Entrez.read(search)
            result = dict(result[0])

            if result["LineageEx"][-1]["Rank"] == "genus":
                bact_genera = result["ScientificName"][-1].lower()
                bact_species = result["ScientificName"].lower()
                resultfile.write(f"{bact_genera} #### {bact_species}")
                currenttaxids.write(f"{}")
                dmp.remove(dmp)
        except:
            failedfile.write(f"{dmp}\n")
        
        time.sleep(0.35)

with open("IndexErrorTaxids.txt", "w") as outfile:
    for failed_taxid in error_ids_list:
        outfile.write(f'{failed_taxid}\n')
