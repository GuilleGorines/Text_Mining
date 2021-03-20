from Bio import Medline
from Bio import Entrez
import sys

idfile = sys.argv[1]
corpora_name = f"{sys.argv[2]}_corpora.txt"
logfile = f"{sys.argv[2]}_corpora.log"

Entrez.max_tries=15
Entrez.email="" # Necesario o error

with open(idfile,"r") as idlist:
    idlist = idlist.readlines()

with open(corpora_name,"w") as corpora, open(logfile,"w") as corporalog:
    for single_id in idlist:
        try:
            search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
            record = list(Medline.parse(search))
            record = dict(record[0])
            pmid = record["PMID"]
            date = record["DP"]
            record = record["AB"]

            corporalog.write(f"{single_id}@success")
            corpora.write(f'{date.lower()} @|@ {pmid.lower()} @|@ {record.lower()}\n')

        except:
            corporalog.write(f"{single_id}@failed")

