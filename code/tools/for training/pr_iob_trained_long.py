# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 01:01:57 2019

@author: Αλέξανδρος
"""

from itertools import zip_longest
import time
import os

start_time = time.time()

name = 'arizona'

ents1 = []
texts1 = []
ents2 = []
texts2 = []

types = set()
#find how many entity types there are
with open("1. test iob\\" + name + ".iob2", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.strip('\n')
        line = line.split('\t')#split string to id, etity type, start end, entity
        
        if len(line) > 1 :
            types.add(line[1])
            
        line = fi.readline()

types = list(types) #turn set into list for indexing
types.sort()

tp = []  #true positives
retrieved = []
relevant = []

for i in types:
    tp.append(0)
    retrieved.append(0)
    relevant.append(0)
    
num = 0

with open("3. abner iob trained\\" + name + ".iob2", encoding="utf-8") as fi1, open("1. test iob\\" + name + ".iob2", encoding="utf-8") as fi2:
    
    for line1, line2 in zip_longest(fi1, fi2):
        
        if line1 != None and len(line1.split('\t')) > 1:
            line1 = line1.lower()# to make easier the comparison of strings
            line1 = line1.strip('\n')
            line1 = line1.split("\t")#to get entity type(ent) and entity(text)
                
            ent = line1[1]
            text = line1[0]
            
            cond = True
            try: #in order to handle the case in which an entity type was found that does not exists in the _test file
                retrieved[types.index(ent)] += 1
            except ValueError:
                cond = False
                
            if cond: #put them in the list only if the entity type exists
                ents1.insert(0, ent)
                texts1.insert(0, text)
            
            
        if line2 != None and len(line2.split('\t')) > 1:  
            print(num)#just to check progress, what line of the text are we at
            num += 1
            
            line2 = line2.lower()
            line2 = line2.strip('\n')
            line2 = line2.split("\t")
            
            ent = line2[1]
            text = line2[0]
            
            type_index = types.index(ent)
            relevant[type_index] += 1
            
            #check if the current line is found by the NER program
            if text in texts1:
                index = texts1.index(text)
                tmp = ents1[ index ]
                
                del texts1[index]
                del ents1[index]
                
                if ent == tmp:
                    tp[type_index] += 1
                else:
                    ents2.insert(0, ent)
                    texts2.insert(0, text)
                
                
#check the remainings of the lists
if len(ents1)>0 and len(ents2)>0:
    for i in range(0, len(ents2)):
        text = texts2[i]
        ent = ents2[i]
        if text in texts1:
            index = texts1.index(text)
            tmp = ents1[ index ]
            
            del texts1[index]
            del ents1[index]
            
            if ent == tmp:
                tp[type_index] += 1
                
#for micro and macro average
relevant_sum = sum(relevant)#sum of all relevant
retrieved_sum = sum(retrieved)#sum of all retrieved
tps = 0 # sum of all tp
prec = 0 #sum of all precisions
rec = 0 #sum of all recalls
#for weighted average
weighted_p = 0 
weighted_r = 0
total = len(types) #total number of classes, 2 for each ett entry(B and I) and +1 for O

if os.path.exists("4. abner results\\" + name + "_iob.txt"):
    os.remove("4. abner results\\" + name + "_iob.txt")

#due to the large number of entities we write the results on a file
output = open("4. abner results\\" + name + "_iob.txt", "a", encoding="utf8")

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
    tps += tp[i]
    prec += precision
    rec += recall
    #for weighted average
    weighted_p += ( precision * ( retrieved[i] / retrieved_sum ) )
    weighted_r += ( recall * ( relevant[i] / relevant_sum ) )
    
    output.write("{}: \n".format(types[i]))
    output.write("\tPrecision: {}\n".format(precision))
    output.write("\tRecall: {}\n".format(recall))
    output.write("\tF1: {}\n".format(f1))
    #for micro and macro average
    output.write("\tTrue Positives: {}\n".format(tp[i]))
    output.write("\tRetrieved: {}\n".format(retrieved[i]) )
    output.write("\tRelevant: {}\n".format(relevant[i]) ) 
    

#micro average
mi_pre = tps/retrieved_sum
mi_rec = tps/relevant_sum
mi_f1 = (2 * mi_pre * mi_rec) / (mi_pre + mi_rec)
output.write("Micro Average: \n")
output.write("\tPrecision: {}\n".format(mi_pre))
output.write("\tRecall: {}\n".format(mi_rec))
output.write("\tF1: {}\n".format(mi_f1))
    
#macro average
ma_pre = prec/total
ma_rec = rec/total
ma_f1 = (2 * ma_pre * ma_rec) / (ma_pre + ma_rec)
output.write("Macro Average: \n")
output.write("\tPrecision: {}\n".format(ma_pre))
output.write("\tRecall: {}\n".format(ma_rec))
output.write("\tF1: {}\n".format(ma_f1))

#weighted average
we_pre = weighted_p
we_rec = weighted_r
we_f1 = (2 * we_pre * we_rec) / (we_pre + we_rec)
output.write("Weighted Average: \n")
output.write("\tPrecision: {}\n".format(we_pre))
output.write("\tRecall: {}\n".format(we_rec))
output.write("\tF1: {}\n".format(we_f1))

output.write("{}\n".format(time.time() - start_time))

output.close()