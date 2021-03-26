#!/bin/bash
if [ ! -e categories.dmp ];
then
    wget --quiet ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip
    unzip -qq -o taxcat.zip
    rm -rf taxcat.zip
    awk '$1 == "B" {print $2}' categories.dmp > tmp
    uniq tmp > categories.dmp
else
    echo "Ya existe un categories.dmp"
fi



printf "%bcategories.dmp descargado y extraido exitosamente. \n"


declare -a QUERYLIST=("digimon" "medibots")

for word in ${QUERYLIST[@]};
do
    printf "%bExtrayendo corpora para la query ${word}. \n"
    python bin/Extract_corpora.py $word $word
done
printf "%bExtracción de corporas exitosa. \n"

printf "%b$(date +"%H:%M"): Se inicia la unión de corporas. \n"
python bin/Merge_corporas.py *_corpora.txt

printf "%b$(date +"%H:%M"): Se inicia la descarga del diccionario de enfermedades. \n"
python bin/Extract_disease_dict.py

printf "%b$(date +"%H:%M"): Se inicia la descarga del diccionario de bacterias. \n"
python bin/Extract_bact_dict.py categories.dmp

printf "%b$(date +"%H:%M"): Se inicia la comparación. \n"
python bin/Perform.py bact_dict.json diseases_dict.json Final_corpora.txt