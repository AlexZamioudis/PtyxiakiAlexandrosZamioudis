# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 18:34:44 2019

@author: Αλέξανδρος
"""
import time

start_time = time.time()

ents = []
texts = []
#PROTEIN, DNA, RNA, CELL_TYPE, CELL_LINE
ett = [ "Protein", "DNA", "RNA", "Cell Type", "Cell Line" ]
tpB = [0, 0, 0, 0, 0]  #true positives
tpI = [0, 0, 0, 0, 0]
tpO = 0
retrievedB = [0, 0, 0, 0, 0]
retrievedI = [0, 0, 0, 0, 0]
retrievedO = 0
with open("3. abner iob\\cellfinder.iob2",  encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.split("\t")#to get entity type(ent) and entity(text)
        
        if len(line) <= 1: #check for empty lines
            line = fi.readline()
            continue
        
        ent = line[1]
        #get retrieved for precision
        if ent[0] == "o": #check if entity is O
            retrievedO += 1
        else:
            #not elif as there can be multiple types per entity
            #check if the enity is B or I
            if "protein" in ent:
                if ent[0] == "b":
                    retrievedB[0] += 1
                else:
                    retrievedI[0] += 1
            if "dna" in ent:
                if ent[0] == "b":
                    retrievedB[1] += 1
                else:
                    retrievedI[1] += 1
            if "rna" in ent:
                if ent[0] == "b":
                    retrievedB[2] += 1
                else:
                    retrievedI[2] += 1
            if "cell_type" in ent or "celltype" in ent or "cell type" in ent:
                if ent[0] == "b":
                    retrievedB[3] += 1
                else:
                    retrievedI[3] += 1
            if "cell_line" in ent or "cellline" in ent or "cell line" in ent:
                if ent[0] == "b":
                    retrievedB[4] += 1
                else:
                    retrievedI[4] += 1
        
        text = line[0]
        
        ents.append(ent)
        texts.append(text)
        
        line = fi.readline()
        
relevantB = [0, 0, 0, 0, 0]
relevantI = [0, 0, 0, 0, 0]
relevantO = 0

num = 0
with open("1. iob\\cellfinder.iob2",  encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        print(num) #just to check progress, what line of the text are we at
        num += 1
        line = line.lower()
        line = line.split("\t")
        
        if len(line) <= 1: #check for empty lines
            line = fi.readline()
            continue
        
        ent = line[1]
        #get the relevants for recall
        if ent[0] == "o":
            relevantO += 1
        else:
            #not elif as there can be multiple types per entity
            if "protein" in ent:
                if ent[0] == "b":
                    relevantB[0] += 1
                else:
                    relevantI[0] += 1
            if "dna" in ent:
                if ent[0] == "b":
                    relevantB[1] += 1
                else:
                    relevantI[1] += 1
            if "rna" in ent:
                if ent[0] == "b":
                    relevantB[2] += 1
                else:
                    relevantI[2] += 1
            if "cell_type" in ent or "celltype" in ent or "cell type" in ent:
                if ent[0] == "b":
                    relevantB[3] += 1
                else:
                    relevantI[3] += 1
            if "cell_line" in ent or "cellline" in ent or "cell line" in ent:
                if ent[0] == "b":
                    relevantB[4] += 1
                else:
                    relevantI[4] += 1
        
        text = line[0]
        
        #check if the current line is found by the NER program
        if text in texts:
            index = texts.index(text)
            tmp = ents[ index ]
            
            texts[index] = None #remove the text
            
            if tmp[0] == "o" and ent[0] == "o":
                tpO += 1
            elif tmp[0] != "o" and tmp[0] == ent[0]:
                if "protein" in ent and "protein" in tmp:
                    if tmp[0] == "b":
                        tpB[0] += 1
                    else:
                        tpI[0] += 1
                if "dna" in ent and "dna" in tmp:
                    if tmp[0] == "b":
                        tpB[1] += 1
                    else:
                        tpI[1] += 1
                if "rna" in ent and "rna" in tmp:
                    if tmp[0] == "b":
                        tpB[2] += 1
                    else:
                        tpI[2] += 1
                if ("cell_type" in ent or "celltype" in ent or "cell type" in ent) and ("cell_type" in tmp or "celltype" in tmp or "cell type" in tmp):
                    if tmp[0] == "b":
                        tpB[3] += 1
                    else:
                        tpI[3] += 1
                if ("cell_line" in ent or "cellline" in ent or "cell line" in ent) and ("cell_line" in tmp or "cellline" in tmp or "cell line" in tmp):
                    if tmp[0] == "b":
                        tpB[4] += 1
                    else:
                        tpI[4] += 1

        line = fi.readline()
        
#for micro and macro average
relevant = sum(relevantB) + sum(relevantI) + relevantO #sum of all relevant
retrieved = sum(retrievedB) + sum(retrievedI) + retrievedO #sum of all retrieved
tp = 0 # sum of all tp
prec = 0 #sum of all precisions
rec = 0 #sum of all recalls
#for weighted average
weighted_p = 0 
weighted_r = 0
total = 2*len(ett) + 1 #total number of classes, 2 for each ett entry(B and I) and +1 for O
#print results
for i in range(0, len(ett)):
    #print the B
    if retrievedB[i] == 0 or relevantB[i] == 0 or tpB[i] == 0:
        precision = 0
        recall = 0
        f1 = 0
    else:
        precision = tpB[i]/retrievedB[i]
        recall = tpB[i]/relevantB[i]
        f1 = (2 * precision * recall) / (precision + recall)
    
    #for micro and macro average
    tp += tpB[i]
    prec += precision
    rec += recall
    #for weighted average
    weighted_p += ( precision * ( retrievedB[i] / retrieved ) )
    weighted_r += ( recall * ( relevantB[i] / relevant ) )
    
    print("B-{}: ".format(ett[i]))
    print("\tPrecision: {}".format(precision))
    print("\tRecall: {}".format(recall))
    print("\tF1: {}".format(f1))
    
    print("\tTrue Positives: {}".format(tpB[i]))
    print("\tRelevant: {}".format(relevantB[i]))
    print("\tRetrieved: {}".format(retrievedB[i]))
    
    #print the I
    if retrievedI[i] == 0 or relevantI[i] == 0 or tpI[i] == 0:
        precision = 0
        recall = 0
        f1 = 0
    else:
        precision = tpI[i]/retrievedI[i]
        recall = tpI[i]/relevantI[i]
        f1 = (2 * precision * recall) / (precision + recall)
    
    tp += tpI[i]
    prec += precision
    rec += recall
    #for weighted average
    weighted_p += ( precision * ( retrievedI[i] / retrieved ) )
    weighted_r += ( recall * ( relevantI[i] / relevant ) )
    
    print("I-{}: ".format(ett[i]))
    print("\tPrecision: {}".format(precision))
    print("\tRecall: {}".format(recall))
    print("\tF1: {}".format(f1))
    
    print("\tTrue Positives: {}".format(tpI[i]))
    print("\tRelevant: {}".format(relevantI[i]))
    print("\tRetrieved: {}".format(retrievedI[i]))
    
#print the O
if retrievedO == 0 or relevantO == 0 or tpO == 0:
    precision = 0
    recall = 0
    f1 = 0
else:
    precision = tpO/retrievedO
    recall = tpO/relevantO
    f1 = (2 * precision * recall) / (precision + recall)

#for micro and macro average
tp += tpO
prec += precision
rec += recall
#for weighted average
weighted_p += ( precision * ( retrievedO / retrieved ) )
weighted_r += ( recall * ( relevantO / relevant ) )

print("O: ")
print("\tPrecision: {}".format(precision))
print("\tRecall: {}".format(recall))
print("\tF1: {}".format(f1))

print("\tTrue Positives: {}".format(tpO))
print("\tRelevant: {}".format(relevantO))
print("\tRetrieved: {}".format(retrievedO))

#micro average
mi_pre = tp/retrieved
mi_rec = tp/relevant
mi_f1 = (2 * mi_pre * mi_rec) / (mi_pre + mi_rec)
print("Micro Average: ")
print("\tPrecision: {}".format(mi_pre))
print("\tRecall: {}".format(mi_rec))
print("\tF1: {}".format(mi_f1))
    
#macro average
ma_pre = prec/total
ma_rec = rec/total
ma_f1 = (2 * ma_pre * ma_rec) / (ma_pre + ma_rec)
print("Macro Average: ")
print("\tPrecision: {}".format(ma_pre))
print("\tRecall: {}".format(ma_rec))
print("\tF1: {}".format(ma_f1))

#weighted average
we_pre = weighted_p
we_rec = weighted_r
we_f1 = (2 * we_pre * we_rec) / (we_pre + we_rec)
print("Weighted Average: ")
print("\tPrecision: {}".format(we_pre))
print("\tRecall: {}".format(we_rec))
print("\tF1: {}".format(we_f1))

print(time.time() - start_time)