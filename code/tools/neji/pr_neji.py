# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 16:53:40 2019

@author: Αλέξανδρος
"""

ents = []
texts = []
#genes/proteins, anatomy, disorder
tp = [0, 0, 0]  #true positives
retrieved = [0, 0, 0]
ett = [ "Genes/Proteins", "Anatomy", "Disorders"]

with open("3. neji tags\\scai_disease.txt",  encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        line = line.lower()# to make easier the comparison of strings
        line = line.split("\t")#to get entity type(ent) and entity(text)
        
        ent = line[1]
        #get retrieved for precision
        #not elif as there can be multiple types per entity
        if "protein" in ent or "gene" in ent:
            retrieved[0] += 1
        if "anatomy" in ent:
            retrieved[1] += 1
        if "disorder" in ent:
            retrieved[2] += 1
        
        text = line[4]
        
        ents.append(ent)
        texts.append(text)
        
        line = fi.readline()
        
relevant = [0, 0, 0, 0, 0]
with open("1. annotations\\scai_disease.txt",  encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        
        line = line.lower()
        line = line.split("\t")
        
        ent = line[1]
        #get the relevants for recall
        if "protein" in ent or "gene" in ent:
            relevant[0] += 1
        if "anatomy" in ent:
            relevant[1] += 1
        if "disorder" in ent:
            relevant[2] += 1
        
        text = line[4]
        
        #check if the current line is found by the NER program
        if text in texts:
            index = texts.index(text)
            tmp = ents[ index ]
            
            del texts[index]#remove the text
            del ents[index]
            
            if ("protein" in ent or "gene" in ent) and ("protein" in tmp or "gene" in tmp):
                tp[0] += 1
            if "anatomy" in ent and "anatomy" in tmp:
                tp[1] += 1
            if "disorder" in ent and "disorder" in tmp:
                tp[2] += 1
                
        
        line = fi.readline()


#for micro and macro average
relevant_sum = sum(relevant)#sum of all relevant
retrieved_sum = sum(retrieved)#sum of all retrieved
tp_sum = 0 # sum of all tp
prec = 0 #sum of all precisions
rec = 0 #sum of all recalls
#for weighted average
weighted_p = 0 
weighted_r = 0
total = len(ett)
#print results
for i in range(0, len(ett)):
    
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
    
    print("{}: ".format(ett[i]))
    print("\tPrecision: {}".format(precision))
    print("\tRecall: {}".format(recall))
    print("\tF1: {}".format(f1))
    #for micro and macro average
    print("\tTrue Positives: {}".format(tp[i]))
    print("\tFalse Positives: {}".format( abs(tp[i] - retrieved[i]) ))
    print("\tFalse Negatives: {}".format( abs(tp[i] - relevant[i]) )) 

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
print("Micro Average: ")
print("\tPrecision: {}".format(mi_pre))
print("\tRecall: {}".format(mi_rec))
print("\tF1: {}".format(mi_f1))
    
#macro average
ma_pre = prec/total
ma_rec = rec/total

if (ma_pre + ma_rec) != 0:
    ma_f1 = (2 * ma_pre * ma_rec) / (ma_pre + ma_rec)
else:
    ma_f1 = 0

print("Macro Average: ")
print("\tPrecision: {}".format(ma_pre))
print("\tRecall: {}".format(ma_rec))
print("\tF1: {}".format(ma_f1))

#weighted average
we_pre = weighted_p
we_rec = weighted_r

if (we_pre + we_rec) != 0:
    we_f1 = (2 * we_pre * we_rec) / (we_pre + we_rec)
else:
    we_f1 = 0

print("Weighted Average: ")
print("\tPrecision: {}".format(we_pre))
print("\tRecall: {}".format(we_rec))
print("\tF1: {}".format(we_f1))
  
