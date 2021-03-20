#!/bin/bash

python bin/Extract_corpora_ids.py "bacteremia or sepsis or septicemia" "septic"
python bin/Extract_corpora_from_ids "septic_ids.txt" "septic"