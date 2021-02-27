import json
import sys

def extract_key_from_value(dictionary, query):
  for key, values in dictionary.items():
      for synonim in values:
          if query == synonim:
              return key
 
bact_dict = json.loads(sys.argv[1])
disease_dict = json.loads(sys.argv[2])
corpora_file = sys.argv[3]

with open(corpora_file) as corpora:
    abstracts = corpora.readlines().split(" @|@ ")


recuento_enfermedades = {}
recuento_bacterias_spp = {}
recuento_bacterias_genus = {}

abstracts_with_bacteria = 0
abstracts_with_disease = 0
abstracts_with_both_bacteria_disease = 0
abstracts_with_none = 0

with open("Abstract_coincidences.txt","w") as abstract_analysis:
    for num, abstract in enumerate(abstracts):
        recount = [num, abstract[0]]
        species_list_abstract = []

        for genus in list(bact_dict.keys()):
            if genus in abstract[1]:
                if genus not in recuento_bacterias_genus.keys():
                    recuento_bacterias_genus[genus]=[1,[]]
                    recuento_bacterias_genus[genus][1].append(abstract[0])
                else:
                    recuento_bacterias_genus[genus][0]+=1
                    recuento_bacterias_genus[genus][1].append(abstract[0])

                for species in bact_dict[genus]:
                    if species in abstract[1]:
                        species_list_abstract.append(species)

                        if species not in recuento_bacterias_spp.keys():
                            recuento_bacterias_spp[species]=[1,[]]
                            recuento_bacterias_spp[species][1].append(abstract[0])
                        else:
                            recuento_bacterias_spp[species][0]+=1
                            recuento_bacterias_spp[species][1].append(abstract[0])

        recount.append(species_list_abstract)

        disease_list_abstract = []

        for disease in list(disease_dict.values()):
            if disease in abstract[1]:
                disease_true = extract_key_from_value(disease_dict, disease)
                disease_list_abstract.append(disease_true)
                if disease_true not in recuento_enfermedades.keys():
                    recuento_enfermedades[disease_true] = [1,[]]
                    recuento_enfermedades[disease_true][1].append(abstract[0])
                else:
                    recuento_enfermedades[disease_true][0] += 1
                    recuento_enfermedades[disease_true][1].append(abstract[0])

        recount.append(disease_list_abstract)

        if len(recount[2]) > 0:
            abstracts_with_bacteria += 1

        if len(recount[3]) > 0:
            abstracts_with_disease += 1

        if len(recount[2]) > 0 and len(recount[3]) > 0:
            abstracts_with_both_bacteria_disease += 1
        
        if len(recount[2]) == 0 and len(recount[3]) == 0:
            abstracts_with_none += 1

        abstract_analysis.write(f'{tuple(recount)}\n')
    
with open("Report.txt","w") as outfile:
    outfile.write(f"La cantidad inicial de abstracts es {len(abstracts)}. \n  \
        Hay un total de {abstracts_with_bacteria} abstracts que mencionan bacterias y NO enfermedades. \n\
        Hay un total de {abstracts_with_disease} abstracts que mencionan enfermedades SIN mencionar bacterias. \n\
        Hay un total de {abstracts_with_both_bacteria_disease} abstracts que mencionan TANTO bacterias COMO enfermedades. \n\
        Hay un total de {abstracts_with_none} abstracts que NO mencionan bacterias NI enfermedades. \n \n \n \
        La cantidad de especies bacterianas distintas encontradas en los abstracts es de {len(recuento_bacterias_genus.keys())}, procedentes de {len(recuento_bacterias_spp.keys())} géneros. \n \
        La cantidad de enfermedades distintas encontradas en los abstracts es de {len(recuento_bacterias_genus.keys())}.")

# Al final, se generará un archivo en el cual cada línea será una tupla correspondiente a cada uno de los abstracts
with open("recuento_enfermedades.json", "w") as outfile:
    json.dump(recuento_enfermedades, outfile)

with open("recuento_bacterias_spp.json", "w") as outfile:
    json.dump(recuento_bacterias_spp, outfile)

with open("recuento_bacterias_genus.json", "w") as outfile:
    json.dump(recuento_bacterias_genus, outfile)