# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 02:40:17 2019

@author: Αλέξανδρος
"""
import time

start_time = time.time()

ents = []
texts = []
#Genes/Proteins, Anatomy, Disorders
ett = [ "Genes/Proteins", "Anatomy", "Disorders"]
tpO = 0
etype = set()
retrievedO = 0
relevantO = 0
relevant = 0 #sum of all relevant
retrieved = 0 #sum of all retrieved


with open("3. stanford iob\\cellfinder.iob2", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.split("\t")#to get entity type(ent) and entity(text)
        
        if len(line) <= 1: #check for empty lines
            line = fi.readline()
            continue
        
        ent = line[1]
        retrieved += 1
        #get retrieved for precision
        if ent[0] == "o": #check if entity is O
            retrievedO += 1
        else:
            etype.add(ent)#get the types
        
        text = line[0]
        
        ents.append(ent)
        texts.append(text)
        
        line = fi.readline()
       


num = 0
with open("1. iob\\cellfinder.iob2", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        print(num)#just to check progress, what line of the text are we at
        num += 1
        
        line = line.lower()
        line = line.split("\t")
        
        if len(line) <= 1: #check for empty lines
            line = fi.readline()
            continue
        
        ent = line[1]
        relevant += 1
        #get the relevants for recall
        if ent[0] == "o":
            relevantO += 1

        
        text = line[0]
        #check if the current line is found by the NER program
        if text in texts:
            index = texts.index(text)
            tmp = ents[ index ]
            
            del texts[index]
            del ents[index]
            
            if tmp[0] == "o" and ent[0] == "o":
                tpO += 1

        line = fi.readline()

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