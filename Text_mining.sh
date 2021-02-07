QUERY=${1}
DATE=$(date +'%d/%m/%Y')

chmod 777 bin/*

printf("Fecha de comienzo: ${DATE}\n") >> Data_mining.log
printf("${DATE}: se descarga el corpora con la query '${Query}'.") >> Data_mining.log
python bin/Fetch_corpora.py ${QUERY} >> Data_mining.log

DATE=$(date +'%d/%m/%Y, %H:%M')
printf("${DATE}: se genera el diccionario de enfermedades.\n") >> Data_mining.log
python bin/Create_disease_dict.py >> Data_mining.log

DATE=$(date +'%d/%m/%Y, %H:%M')
printf("${DATE}: se genera el diccionario de bacterias.\n") >> Data_mining.log
python bin/Create_bact_dict.py >> Data_mining.log

DATE=$(date +'%d/%m/%Y, %H:%M')
printf("${DATE}: se realiza la búsqueda de términos.\n") >> Data_mining.log
python bin/Search_coincidences.py Corpora.txt Bact_dict.json Disease_dict.json >> Data_mining.log

DATE=$(date +'%d/%m/%Y, %H:%M')
printf("Fecha de finalización: ${DATE}\n") >> Data_mining.log
