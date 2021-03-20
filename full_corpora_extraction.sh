#!/bin/bash
printf "Begin \n"
python bin/Extract_corpora_ids.py "septicemia or bacteremia or sepsis" "septic"
printf "ID extraction completed."
python bin/Extract_corpora_from_ids.py "septic_ids.txt" "septic" > septic_corpora.log
printf "Corpora extraction completed"