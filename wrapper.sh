#!/bin/bash

wget --quiet ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip
unzip -qq -o taxcat.zip
rm -rf taxcat.zip

awk '$1 == "B" {print $3}' categories.dmp > tmp
rm -rf categories.dmp
mv tmp categories.dmp

declare -a QUERYLIST=("" "")

for word in ${QUERYLIST[@]};
do
    echo "Extrayendo corpora para la query ${word}."
    python bin/Extract_corpora.py $word $word
done
printf "%b Extracción de corporas exitosa. \n"

printf "%b $(date +"%H:%M"): Se inicia la unión de corporas. \n"
python bin/Merge_corporas.py *_corpora.txt

printf "%b $(date +"%H:%M"): Se inicia la descarga del diccionario de enfermedades. \n"
python bin/Extract_disease_dict.py

printf "%b $(date +"%H:%M"): Se inicia la descarga del diccionario de bacterias. \n"
python bin/Extract_bact_dict.py categories.dmp

python bin/Perform.py bact_dict.json diseases_dict.json Final_corpora.txt