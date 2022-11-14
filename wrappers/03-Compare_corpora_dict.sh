#!/bin/bash
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Comparison begins.\n"
python3 ../bin/Perform.py diseases_dict.json species_name_dict.json genera_dict.json septic_corpora.txt > comparison.tab
printf "$(date '+%Y-%m-%d, %H:%M:%S') : Comparison was successful.\n"

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Checking stats.\n"

# 1: ID
# 2: Date
# 3: Bacteria genera
# 4: Bacteria species
# 5: Diseases

awk 'BEGIN{
        FS="; ";

        full_data = 0;
        no_data = 0;
        
        only_bacteria = 0;
        only_bacteria_genera = 0;
        only_bacteria_spp = 0;

        only_disease = 0;
        genus_not_spp = 0;
        spp_not_genus = 0;
       
    }

    ($3 != "null" && $4 != "null" && $5 != "null") {full_data += 1}
    ($3 == "null" && $4 == "null" && $5 == "null") {no_data += 1}


    ($3 != "null" && $4 != "null" && $5 == "null") {only_bacteria += 1}
    ($3 != "null" && $4 == "null" && $5 == "null") {only_bacteria_genera += 1}
    ($3 == "null" && $4 != "null" && $5 == "null") {only_bacteria_spp += 1}

    ($3 == "null" && $4 == "null" && $5 != "null") {only_disease += 1}

    ($3 != "null" && $4 == "null" && $5 != "null") {genus_not_spp += 1}
    ($3 == "null" && $4 != "null" && $5 != "null") {spp_not_genus += 1} 
    ($3 == "null" && $4 != "null" && $5 != "null") {print $0}
    END{

        print "Abstracts containing bacteria genera, spp and diseases: " full_data;
        print "Abstracts containing NEITHER bacteria genera, spp or diseases : " no_data;

        print "Abstracts containing bacteria genera and spp BUT NO diseases: " only_bacteria;
        print "Abstracts containing bacteria genera BUT NO bacteria spp or diseases: " only_bacteria_genera;
        print "Abstracts containing bacteria species BUT NO bacteria genera or diseases: " only_bacteria_spp;

        print "Abstracts containing ONLY diseases, NO bacteria genera or spp: " only_disease;

        print "Abstracts containing diseases and bacteria at genus level, but no species level: " genus_not_spp;
        print "Abstracts containing diseases and bacteria at species level, but no genus level: " spp_not_genus;
    } ' comparison.tab

printf "$(date '+%Y-%m-%d, %H:%M:%S') : Stats checking ended.\n"