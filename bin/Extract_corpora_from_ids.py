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

id_status = []
with open(corpora_name,"w") as corpora:
    for single_id in idlist:
        try:
            search = Entrez.efetch(db="pubmed", id=single_id, rettype="medline", retmode="text")
            record = list(Medline.parse(search))
            record = dict(record[0])
            pmid = record["PMID"]
            date = record["DP"]
            record = record["AB"]
            single_id = single_id.replace("\n","")
            corpora.write(f'{date.lower()} @|@ {pmid.lower()} @|@ {record.lower()}\n')
            print(f"{single_id}@success")
            id_status.append(f"{single_id}@success")

        except:
            print(f"{single_id}@failure")
            id_status.append(f"{single_id}@failure")

with open(logfile,"w") as corporalog:
    for status in id_status:
        corporalog.write(f"{status}\n")

