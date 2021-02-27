#!/bin/bash

wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.zip
zip -d taxcat taxcat.zip
rm -rf taxcat.zip
mv taxcat/categories.dmp categories.dmp

awk "$1 == 'B' {print $3}" categories.dmp > tmp
rm -rf categories.dmp
mv tmp categories.dmp

declare -a QUERYLIST = ("" "")

for word in ${QUERYLIST[@]};
do
    python bin/Extract_corpora.py $word
done

python bin/Merge_corporas.py *_corpora.txt
python bin/Extract_disease_dict.py
python bin/Extract_bact_dict.py

python bin/Perform.py bact_dict.json diseases_dict.json Final_corpora.txt