#!/bin/bash
printf "$(date '+%Y%m%d%H%M%S'): ID extraction begins\n"
python3 ../bin/Extract_corpora_ids.py "septicemia or bacteremia or sepsis" "septic"
printf "$(date '+%Y%m%d%H%M%S'): ID extraction completed.\n"
printf "$(date '+%Y%m%d%H%M%S'): Corpora extraction begins.\n"
python3 ../bin/Extract_corpora_from_ids.py "septic_ids.txt" "septic"
printf "$(date '+%Y%m%d%H%M%S'): Corpora extraction completed"