import sys

if len(sys.argv) < 1:
    sys.exit

first_corpora_file = sys.argv[1]
filelist = sys.argv[2:]
headers = []
total_files = len(sys.argv) - 1

with open(first_corpora_file,"r") as first:
    full_corpora = first.readlines()
    headers.append(full_corpora[0])
    full_corpora =[text.split(" @|@ ") for text in full_corpora[1:]]

for file in filelist:
    with open(file,"r") as corpora:
        other_corpora = corpora.readlines()
        headers.append(other_corpora[0])
        other_corpora =[text.split(" @|@ ") for text in other_corpora[1:]]
        full_corpora.append(other_corpora)

full_corpora = set(full_corpora)
total = len(full_corpora)

with open("Corpora_data.txt","w") as corpora_data:
    corpora_data.write(f"La cantidad total de abstracts distintos procedente de estos {total_files} términos distintos es de {total}.\n")
    for header in headers:
        corpora_data.write(f"{header}\n")

with open("Final_corpora.txt","w") as final:
    for date,abstract in full_corpora:
        final.write(f'{date} @|@ {abstract}\n')
