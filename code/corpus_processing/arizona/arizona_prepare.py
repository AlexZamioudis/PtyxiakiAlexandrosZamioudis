# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 16:10:25 2019

@author: Αλέξανδρος
"""
import os

if os.path.exists("1. texts\\arizona.txt"):
    os.remove("1. texts\\arizona.txt")

if os.path.exists("1. annotations\\arizona.txt"):
    os.remove("1. annotations\\arizona.txt")

output1 = open("1. texts\\arizona.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\arizona.txt", "a") #results in order to evaluate NER

num = 0
with open("arizona disease.txt") as fi:  
   
    ids = set() # in order to deal with duplicates
    
    line = fi.readline()
    line = fi.readline()
    
    while line:
        
        line = line.split('\t')
        
        #if Doc is the same, the lines have the same text
        if line[0] not in ids:
            ids.add(line[0])
            output1.write("{}\n".format(line[3]))
        
        #if there is a term in that line's text
        if line[5] and line[5]!='0':
            num += 1
            output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, 'disease', line[4], line[5], line[7]))
        
        line = fi.readline()
        
output1.close()
output2.close()