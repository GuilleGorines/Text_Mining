#!/bin/bash
if [ ! -e categories.dmp ];
then
    wget -O dmp.zip ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip 
    unzip -qq -o dmp.zip
    rm -rf dmp.zip
    awk '$1 == "B" {print $2}' categories.dmp > tmp
    uniq tmp > categories.dmp
    rm -rf tmp
else
    echo "Ya existe un categories.dmp"
fi

printf "%b$(date +"%H:%M"): categories.dmp descargado y extraido exitosamente. \n"

printf "%b$(date +"%H:%M"): Extrayendo corpora para la query. \n"
python bin/Extract_corpora_ids.py "septicemia or bacteremia or sepsis" "septic"

printf "%b$(date +"%H:%M"): ID extraction completed.\n"
python bin/Extract_corpora_from_ids.py "septic_ids.txt" "septic"

printf "%b$(date +"%H:%M")_ Extracción de corporas exitosa. \n"

printf "%b$(date +"%H:%M"): Se inicia la unión de corporas. \n"
python bin/Merge_corporas.py *_corpora.txt

printf "%b$(date +"%H:%M"): Se inicia la descarga del diccionario de enfermedades. \n"
python bin/Extract_disease_dict.py

printf "%b$(date +"%H:%M"): Se inicia la descarga del diccionario de bacterias. \n"
python bin/Extract_bact_dict.py categories.dmp

printf "%b$(date +"%H:%M"): Se inicia la comparación. \n"
python bin/Perform.py bact_dict.json diseases_dict.json Final_corpora.txt
