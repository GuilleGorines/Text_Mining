#!/../bin/bash
if [ ! -e categories.dmp ];
then
    wget -O categories.zip ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip 
    unzip -qq -o categories.zip
    rm -rf categories.zip
    awk '$1 == "B" {print $2}' categories.dmp > tmp
    uniq tmp > categories.dmp
    rm -rf tmp
    printf "$(date '+%Y-%m-%d, %H:%M:%S') : categories.dmp succesfully downloaded and extracted. \n"

else
    echo "$(date '+%Y-%m-%d, %H:%M:%S') : categories.dmp already detected in the directory.\n"
fi

if [ ! -e names.dmp ];
then
    wget -O names.zip https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
    unzip -j names.zip "names.dmp" -d .
    rm -rf names.zip
    printf "$(date '+%Y-%m-%d, %H:%M:%S') : names.dmp successfully downloaded and extracted. \n"

else
    echo "$(date '+%Y-%m-%d, %H:%M:%S') : names.dmp already detected in the directory.\n"
fi


printf "$(date '+%Y-%m-%d, %H:%M:%S') : ID extraction begins.\n"
python3 ../bin/Extract_corpora_ids.py "septicemia or bacteremia or sepsis" "septic"
printf "$(date '+%Y-%m-%d, %H:%M:%S') : ID extraction completed.\n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Corpora extraction begins.\n"
python3 ../bin/Extract_corpora_from_ids.py "septic_ids.txt" "septic"
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Corpora extraction completed.\n"

printf "%b$(date +"%H:%M") : Corpora extraction was successful.\n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Starting corpora union. \n"
python3 ../bin/Merge_corporas.py *_corpora.txt
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Corpora union was successful. \n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Disease dict download begins.\n"
python3 ../bin/Extract_disease_dict.py
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Disease dict download was successful.\n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Bacteria dict download begins.\n"
python3 ../bin/Extract_bactdict_from_dmps.py categories.dmp names.dmp
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Bacteria dict download was successful.\n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Comparison begins.\n"
python3 ../bin/Perform.py bact_dict.json diseases_dict.json Final_corpora.txt
