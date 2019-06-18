# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:12:56 2019

@author: Αλέξανδρος
"""
import os

name = 'scai_disease'

ents = []
texts = []

types = set()
#find how many entity types there are
with open("1. train test 2\\" + name + "_test.ann", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.strip('\n')
        line = line.split('|')#split string to id, etity type, start end, entity
        
        if len(line) > 1 :
            types.add(line[1])
            
        line = fi.readline()

types = list(types) #turn set into list for indexing

tp = []  #true positives
retrieved = []
relevant = []

for i in types:
    tp.append(0)
    retrieved.append(0)
    relevant.append(0)

with open("3. banner tags\\" + name + ".txt", encoding="utf-8") as fi:
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.strip('\n')
        line = line.split('\t')#split string to id, etity type, start end, entity
        
        if len(line) > 1 :
            etype = line[1]
            cond = True
            try: #in order to handle the case in which an entity type was found that does not exists in the _test file
                retrieved[types.index(etype)] += 1
            except ValueError:
                cond = False
                
            if cond: #put them in the list only if the entity type exists
                ents.append(etype)
                texts.append(line[4])
             
        line = fi.readline()

with open("1. train test 2\\" + name + "_test.ann", encoding="utf-8") as fi:
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.strip('\n')
        line = line.split('|')#split string to id, etity type, start end, entity
        
        if len(line) > 1 :
            etype = line[1]
            type_index = types.index(etype)
            relevant[type_index] += 1
            
            text = line[3]
            
            if text in texts:
                index = texts.index(text)
                tmp = ents[index]
                
                del texts[index]
                del ents[index]
            
                if etype == tmp:
                    tp[type_index] += 1
             
        line = fi.readline()

if os.path.exists("4. banner results\\" + name + "_tags.txt"):
    os.remove("4. banner results\\" + name + "_tags.txt")

#due to the large number of entities we write the results on a file
output = open("4. banner results\\" + name + "_tags.txt", "a", encoding="utf8")

#for micro and macro average
relevant_sum = sum(relevant)#sum of all relevant
retrieved_sum = sum(retrieved)#sum of all retrieved
tp_sum = 0 # sum of all tp
prec = 0 #sum of all precisions
rec = 0 #sum of all recalls
#for weighted average
weighted_p = 0 
weighted_r = 0
total = len(types)
#print results
for i in range(0, len(types)):
    
    if retrieved[i] == 0 or relevant[i] == 0 or tp[i] == 0:
        precision = 0
        recall = 0
        f1 = 0
    else:
        precision = tp[i]/retrieved[i]
        recall = tp[i]/relevant[i]
        f1 = (2 * precision * recall) / (precision + recall)
    
    #for micro and macro average
    tp_sum += tp[i]
    prec += precision
    rec += recall
    #for weighted average
    if retrieved_sum != 0:
        weighted_p += ( precision * ( retrieved[i] / retrieved_sum ) )
    else:
        weighted_p += 0
    
    if relevant_sum != 0:
        weighted_r += ( recall * ( relevant[i] / relevant_sum ) )
    else:
        weighted_r += 0
    
    output.write("{}: \n".format(types[i]))
    output.write("\tPrecision: {}\n".format(precision))
    output.write("\tRecall: {}\n".format(recall))
    output.write("\tF1: {}\n".format(f1))
    #for micro and macro average
    output.write("\tTrue Positives: {}\n".format(tp[i]))
    output.write("\tFalse Positives: {}\n".format( abs(tp[i] - retrieved[i]) ))
    output.write("\tFalse Negatives: {}\n".format( abs(tp[i] - relevant[i]) )) 

#micro average
if retrieved_sum != 0:
    mi_pre = tp_sum/retrieved_sum
else:
    mi_pre = 0
    
if relevant_sum != 0:
    mi_rec = tp_sum/relevant_sum
else:
    mi_rec = 0

if (mi_pre + mi_rec) != 0:
    mi_f1 = (2 * mi_pre * mi_rec) / (mi_pre + mi_rec)
else:
    mi_f1 = 0
output.write("Micro Average: \n")
output.write("\tPrecision: {}\n".format(mi_pre))
output.write("\tRecall: {}\n".format(mi_rec))
output.write("\tF1: {}\n".format(mi_f1))
    
#macro average
ma_pre = prec/total
ma_rec = rec/total

if (ma_pre + ma_rec) != 0:
    ma_f1 = (2 * ma_pre * ma_rec) / (ma_pre + ma_rec)
else:
    ma_f1 = 0

output.write("Macro Average: \n")
output.write("\tPrecision: {}\n".format(ma_pre))
output.write("\tRecall: {}\n".format(ma_rec))
output.write("\tF1: {}\n".format(ma_f1))

#weighted average
we_pre = weighted_p
we_rec = weighted_r

if (we_pre + we_rec) != 0:
    we_f1 = (2 * we_pre * we_rec) / (we_pre + we_rec)
else:
    we_f1 = 0

output.write("Weighted Average: \n")
output.write("\tPrecision: {}\n".format(we_pre))
output.write("\tRecall: {}\n".format(we_rec))
output.write("\tF1: {}\n".format(we_f1))


output.close()