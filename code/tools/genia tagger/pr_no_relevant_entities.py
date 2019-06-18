# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 03:05:44 2019

@author: Αλέξανδρος
"""

texts = []

tp = 0
retrieved = 0
with open("3. neji tags\\scai_disease.txt", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        #get retrieved for precision
        retrieved += 1
        line = line.lower()# to make easier the comparison of strings
        line = line.split("\t")#to get entity(text)
        
        text = line[4]
        
        texts.append(text)
        
        line = fi.readline()
        
relevant = 0
with open("1. annotations\\scai_disease.txt", encoding="utf-8") as fi:
    
    line = fi.readline()
    
    while line:
        #get the relevants for recall
        relevant += 1
        line = line.lower()
        line = line.split("\t")
        
        text = line[4]
        #check if the current line is found by the NER program
        if text in texts:
            tp += 1
            del texts[ texts.index(text) ]
            
        line = fi.readline()

#printing results
if retrieved == 0 or relevant == 0 or tp == 0:
    precision = 0
    recall = 0
    f1 = 0
else:
    precision = tp/retrieved
    recall = tp/relevant
    f1 = (2 * precision * recall) / (precision + recall)

print("Precision: {}".format(precision))
print("Recall: {}".format(recall))
print("F1: {}".format(f1))
#for micro and macro average
print("True Positives: {}".format(tp))
print("False Positives: {}".format( abs(tp - retrieved) ))
print("False Negatives: {}".format( abs(tp - relevant) ))