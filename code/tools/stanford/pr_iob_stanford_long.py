# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 01:08:51 2019

@author: Αλέξανδρος
"""


from itertools import zip_longest
import time

start_time = time.time()

ents1 = []
texts1 = []
ents2 = []
texts2 = []
tpO = 0 #true positives
retrievedO = 0
relevantO = 0
etype = set()
relevant = 0 #sum of all relevant
retrieved = 0 #sum of all retrieved

num = 0

with open("3. calais iob\\cemp.iob2", encoding="utf-8") as fi1, open("1. iob\\cemp.iob2", encoding="utf-8") as fi2:
    
    for line1, line2 in zip_longest(fi1, fi2):
    
        if line1 != None and len(line1.split('\t')) > 1:
            line1 = line1.lower()# to make easier the comparison of strings
            line1 = line1.split("\t")#to get entity type(ent) and entity(text)
            
            ent = line1[1]
            retrieved += 1
            #get retrieved for precision
            if ent[0] == "o": #check if entity is O
                retrievedO += 1
            else:
                etype.add(ent)#get the types
            
            text = line1[0]
            
            ents1.insert(0, ent)
            texts1.insert(0, text)
             
        if line2 != None and len(line2.split('\t')) > 1:  
            print(num)#just to check progress, what line of the text are we at
            num += 1
            line2 = line2.lower()
            line2 = line2.split("\t")
            
            ent = line2[1]
            
            relevant += 1
            #get the relevants for recall
            if ent[0] == "o":
                relevantO += 1
            
            text = line2[0]
            #check if the current line is found by the NER program
            if text in texts1:
                index = texts1.index(text)
                tmp = ents1[ index ]
                
                del texts1[index]
                del ents1[index]
                
                if tmp[0] == "o" and ent[0] == "o":
                    tpO += 1
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
                
            if tmp[0] == "o" and ent[0] == "o":
                tpO += 1


#for micro and macro average
#since only the Os are non zero we just use their metrics
total = len(etype) + 1 #total number of classes, 2 for each etype entry(B and I) and +1 for O        
#print results
#print the O
if retrievedO == 0 or relevantO == 0 or tpO == 0:
    precision = 0
    recall = 0
    f1 = 0
else:
    precision = tpO/retrievedO
    recall = tpO/relevantO
    f1 = (2 * precision * recall) / (precision + recall)
    
print("O: ")
print("\tPrecision: {}".format(precision))
print("\tRecall: {}".format(recall))
print("\tF1: {}".format(f1))    

print("\tTrue Positives: {}".format(tpO))
print("\tRelevant: {}".format(relevantO))
print("\tRetrieved: {}".format(retrievedO))
#micro average
mi_pre = tpO/retrieved
mi_rec = tpO/relevant
mi_f1 = (2 * mi_pre * mi_rec) / (mi_pre + mi_rec)
print("Micro Average: ")
print("\tPrecision: {}".format(mi_pre))
print("\tRecall: {}".format(mi_rec))
print("\tF1: {}".format(mi_f1))
    
#macro average
ma_pre = precision/total
ma_rec = recall/total
ma_f1 = (2 * ma_pre * ma_rec) / (ma_pre + ma_rec)
print("Macro Average: ")
print("\tPrecision: {}".format(ma_pre))
print("\tRecall: {}".format(ma_rec))
print("\tF1: {}".format(ma_f1))

#weighted average
weighted_p = ( precision * ( retrievedO / retrieved ) )
weighted_r = ( recall * ( relevantO / relevant ) )

we_pre = weighted_p
we_rec = weighted_r
we_f1 = (2 * we_pre * we_rec) / (we_pre + we_rec)
print("Weighted Average: ")
print("\tPrecision: {}".format(we_pre))
print("\tRecall: {}".format(we_rec))
print("\tF1: {}".format(we_f1))

print(time.time() - start_time)
