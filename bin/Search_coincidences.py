import sys
import json
from pygments.lexers import d

# Funciones necesarias:

def key_from_value(dict, query):
    for key, values in dict.items():
        for synonym in values:
            if query == synonym:
                return key

def back_to_value(dict, query):
    for keys,values in dict.items():
        for key in keys:
            if query == key:
                return value[0]

corpora_file = sys.argv[1]
bact_dict = json.load(sys.argv[2])
dis_dict = json.load(sys.argv[3])

bact_list = [bacteria for sublist in bact_dict.values() for bacteria in sublist]
disease_list = [disease for sublist in dis_dict.values() for disease in sublist]


with open(corpora_file) as full_corpora:
    corpora = [abstract for abstract in corpora_file.readlines()]
 
presences=[]

for num,text in enumerate(corpora):
    coincidences = num
    bacteria_record = []
    disease_record = []

    for bact in bact_list:
        if bact in text:
            taxid = key_from_value(bact_dict,bact)
            bacteria_record.append(taxid)
    for disease in disease_list:
        if disease in text:
            doid = key_from_value(dis_dict,disease)
            disease_record.append(doid)

    if len(bacteria_record) == 0 and len(disease_record) == 0:
        continue # o es pass?
    else:
        presences.append = [num, tuple(bacteria_record), tuple(disease_record)]
