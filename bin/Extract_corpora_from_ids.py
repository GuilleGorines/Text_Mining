from Bio import Medline
from Bio import Entrez
import sys

## Color constants##

green = "\033[32m"
red = "\033[31m"
reset = "\033[0m"


idfile = sys.argv[1]
corpora_name = f"{sys.argv[2]}_corpora.txt"
logfile = f"{sys.argv[2]}_corpora.log"

Entrez.max_tries=15
Entrez.email="" # Necesario o error

with open(idfile,"r") as idlist:
    idlist = idlist.readlines()

id_status = []

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
            corpora.write(f'{date.lower()} @|@ {pmid.lower()} @|@ {record.lower()}\n')
            print(f"{single_id}: {green}success{reset}")
            id_status.append(f"{single_id}: success")
            successful += 1
        
        except:
            print(f"{single_id}: {red}failure{reset}")
            id_status.append(f"{single_id}: failure")
            failed+=1

with open(logfile,"w") as corporalog:
    for status in id_status:
        corporalog.write(f"{status}\n")

    total = successful + failed
    successful_percentage = succesful/total
    failed_percentage = 1-successful_percentage

    final_msg = f"Out of {total} ids, {successful} ({successful_percentage}%) were succesful and {failed} ({failed_percentage}%) failed.\n"
    print(final_msg)
    corporalog.write(final_msg)
