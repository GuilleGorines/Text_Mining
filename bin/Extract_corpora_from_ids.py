#!/usr/bin/env python3

from Bio import Medline
from Bio import Entrez
import sys

## Color constants just in case##

green = "\033[32m"
red = "\033[31m"
reset = "\033[0m"


idfile = sys.argv[1]
corpora_name = f"{sys.argv[2]}_corpora.txt"

Entrez.max_tries=15
Entrez.email="" # Necesario o error

with open(idfile,"r") as idlist:
    idlist = idlist.readlines()

# Counter
successful = 0
failed = 0

with open(corpora_name,"w") as corpora:

    for single_id in idlist:

        single_id = single_id.replace("\n","")
        try:
            search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
            record = list(Medline.parse(search))
            record = dict(record[0])
            pmid = record["PMID"]
            date = record["DP"]
            record = record["AB"]
            corpora.write(f'{single_id} @|@ {date.lower()} @|@ {record.lower()}\n')
            
            successful += 1
            msg = f"{single_id}: success; {successful} abstracts downloaded successfully, {failed} errors."
            print(msg)
        
        except:
            failed+=1
            corpora.write(f'{single_id}:::FAILED ({failed})\n')
            
            msg = f"{single_id}: failure; {successful} abstracts downloaded successfully, {failed} errors."
            print(msg)


total = successful + failed
successful_percentage = successful/total
failed_percentage = 1-successful_percentage

final_msg = f"Out of {total} ids, {successful} ({successful_percentage}%) were succesful and {failed} ({failed_percentage}%) failed.\n"
print(final_msg)
