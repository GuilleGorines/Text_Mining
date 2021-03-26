import json
import sys

def extract_key_from_value(dictionary, query):
  for key, values in dictionary.items():
      for synonim in values:
          if query == synonim:
              return key
 
disease_dict = json.loads(sys.argv[1])
spp_dict = json.loads(sys.argv[2])
genera_dict = json.loads(sys.argv[3])
corpora_file = sys.argv[4]

with open(corpora_file) as corpora:
    abstracts = corpora.readlines().split(" @|@ ")

spp_mentioned = {}
genus_mentioned = {}
diseases_mentioned = {}
abstracts_data_full = []


for num, full_abstract in abstracts:
    print(num)
    # date, id, species, genera, diseases
    abstract_data = [full_abstract[0],full_abstract[1],[],[],[]]
    for spp_name in spp_dict.values():
        if spp_name in full_abstract[2]:
            spp_key = extract_key_from_value(spp_dict,spp_name)
            abstract_data[2].append(spp_name)

            if spp_key not in spp_mentioned.keys():
                spp_mentioned[spp_key] = 1
            else:
                spp_mentioned[spp_key] += 1

            genus_key = extract_key_from_value(genera_dict,spp_key)
            abstract_data[3].append(spp_name)

            if genus_key not in genus_mentioned.keys():
                genus_mentioned[genus_key] = 1
            else:
                genus_mentioned[genus_key] += 1
    
    for disease_name in disease_dict.values():
        if disease_name in full_abstract[2]:
            disease_key = extract_key_from_value(disease_name)
            abstract_data[3].append(disease_key)
            if disease_key not in diseases_mentioned.keys():
                diseases_mentioned[disease_key] = 1
            else:
                diseases_mentioned[disease_key] += 1

    abstracts_data_full.append(abstract_data)


with open("recounts.txt","w") as recountfile:
    for abstract_recount in abstracts_data_full:
        date = abstract_recount[0]
        pmid = abstract_recount[1]
        spps = abstract_recount[2]
        genus = abstract_recount[3]
        disease = abstract_recount[4]
        writestring = f"{date} @|@ {pmid} @|@ {spps} @|@ {genus} @|@ {disease}" 
        recountfile.write(writestring)

abstracts_with_bacteria = 0
abstracts_with_disease = 0
abstracts_with_both_bacteria_disease = 0
abstracts_with_none = 0

# date, id, species, genera, diseases

for recount in abstracts_data_full:
    if len(recount[2]) > 0:
        abstracts_with_bacteria += 1

    if len(recount[4]) > 0:
        abstracts_with_disease += 1

    if len(recount[2]) > 0 and len(recount[4]) > 0:
        abstracts_with_both_bacteria_disease += 1
    
    if len(recount[2]) == 0 and len(recount[4]) == 0:
        abstracts_with_none += 1
    
with open("Report.txt","w") as outfile:
    outfile.write(f"La cantidad inicial de abstracts es {len(abstracts)}. \n  \
        Hay un total de {abstracts_with_bacteria} abstracts que mencionan bacterias y NO enfermedades. \n\
        Hay un total de {abstracts_with_disease} abstracts que mencionan enfermedades SIN mencionar bacterias. \n\
        Hay un total de {abstracts_with_both_bacteria_disease} abstracts que mencionan TANTO bacterias COMO enfermedades. \n\
        Hay un total de {abstracts_with_none} abstracts que NO mencionan bacterias NI enfermedades. \n \n \n \
        La cantidad de especies bacterianas distintas encontradas en los abstracts es de {len(spp_mentioned.keys())}, procedentes de {len(genus_mentioned.keys())} géneros. \n \
        La cantidad de enfermedades distintas encontradas en los abstracts es de {len(diseases_mentioned.keys())}.")

# Al final, se generará un archivo en el cual cada línea será una tupla correspondiente a cada uno de los abstracts
with open("Recuento_enfermedades.json", "w") as outfile:
    json.dump(diseases_mentioned, outfile)

with open("Recuento_bacterias_spp.json", "w") as outfile:
    json.dump(spp_mentioned, outfile)

with open("Recuento_bacterias_genus.json", "w") as outfile:
    json.dump(genus_mentioned, outfile)