#!/bin/bash
if [ ! -e categories.dmp ];
then
    wget -O categories.zip ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip 
    unzip -qq -o categories.zip
    rm -rf categories.zip
    awk '$1 == "B" {print $2}' categories.dmp > tmp
    uniq tmp > categories.dmp
    rm -rf tmp
    printf "$(date '+%Y-%m-%d, %H:%M:%S') : categories.dmp descargado y extraido exitosamente. \n"

else
    echo "$(date '+%Y-%m-%d, %H:%M:%S') : Ya existe un categories.dmp"
fi

if [ ! -e names.dmp ];
then
    wget -O names.zip https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
    unzip -j names.zip "names.dmp" -d .
    rm -rf names.zip
    printf "$(date '+%Y-%m-%d, %H:%M:%S') : names.dmp descargado y extraido exitosamente. \n"

else
    echo "$(date '+%Y-%m-%d, %H:%M:%S') : Ya existe un names.dmp"
fi

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Se inicia la descarga del diccionario de enfermedades. \n"
python ../bin/Extract_disease_dict.py
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Descarga del diccionario de enfermedades finalizada. \n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Se inicia la descarga del diccionario de bacterias. \n"
python ../bin/Extract_bactdict_from_dmps.py categories.dmp names.dmp
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Descarga del diccionario de bacterias finalizada. \n"