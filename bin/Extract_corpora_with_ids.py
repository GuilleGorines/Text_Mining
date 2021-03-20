from Bio import Medline
from Bio import Entrez
import sys

idfile = sys.argv[1]
corpora_name = f"{sys.argv[2]}_corpora_recovered.txt"

Entrez.max_tries=5
Entrez.email="" # Necesario o error

with open(idfile,"r") as failedids:
    failedids = failedids.readlines()

with open (corpora_name,"w") as corpora:
    for single_id in failedids:
        try:
            search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
            record = list(Medline.parse(search))
            record = dict(record[0])
            print(f"{single_id}-success")

            pmid = record["PMID"]
            date = record["DP"]
            record = record["AB"]
            cantidad_abstracts += 1

            corpora.write(f'{date.lower()} @|@ {pmid.lower()} @|@ {record.lower()}\n')

        except:
            print(f"{single_id}-failed")

