# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:42:01 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\scai_disease.txt"):
    os.remove("1. texts\\scai_disease.txt")

if os.path.exists("1. annotations\\scai_disease.txt"):
    os.remove("1. annotations\\scai_disease.txt")

output1 = open("1. texts\\scai_disease.txt", "a", encoding="utf8")
output2 = open("1. annotations\\scai_disease.txt", "a", encoding="utf8")


with open("SCAI disease.txt", encoding="utf8") as fi:      
   line = fi.readline()
   
   text = ""
   prev = 0
   
   count = 0
   etype = "" #entity type
   ent = "" #entity
   start = 0 #entity start point
   end = 0 #entity end point
   
   num = 0
   while line:
        line = line.replace('\t\t','\t')#remove double tabs
        line = line.split('\t')
        if len(line) == 1:
            if prev != 0: #change line
                 output1.write("\n")
            prev = 0

            line = fi.readline()
            continue #for the empty lines or ids in the text
        else:
            #add spaces to the text based on current start and previous end
            tmp = int(line[1])-prev
            if tmp < 0:
                tmp = 0
            
            for i in range(0, tmp):
                text += ' '
            text += line[0]
            prev = int(line[2])#the ent of the current token
            output1.write("{}".format(text)) #write the text
            text = ""
        
        if line[3][0] != "|": #in the begining of the entity, the full name is given
            ent = line[3] #get the full entity name
            start = line[1]
            end = int(start) + len(ent)
            #etype = line[4][3:-1]# remove |B- and \n #for training data
            etype = "Disease" #for non trained model comparisons
            num += 1
            output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, etype, start, end, ent))
              
        line = fi.readline()

output1.close()     
output2.close()