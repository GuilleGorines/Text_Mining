#!/bin/bash

python bin/Extract_corpora_ids.py "septicemia or bacteremia or sepsis" "septic"
python bin/Extract_corpora_from_ids "septic_ids.txt" "septic"