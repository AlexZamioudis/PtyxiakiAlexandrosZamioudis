# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 02:37:15 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("3. geniatagger tags\\scai_disease.txt"):
    os.remove("3. geniatagger tags\\scai_disease.txt")

output = open("3. geniatagger tags\\scai_disease.txt", "a", encoding="utf8")

with open("2. geniatagger results\\scai_disease.txt", encoding="utf8") as fi:  
    
   line = fi.readline()
   
   text = ""
   
   etype = "" #entity type
   ent = "" #entity
   start = 0 #entity start point
   end = 0 #entity end point
   
   num = 0
   while line:
        line = line.split('\t')
        
        if len(line) == 1:
            line = fi.readline()
            continue #for the empty lines in the text
        
        if line[4][0] == "O":
            if etype != "":
                ent = ent[:-1] #minus 1 for the space after the last word
                end = start +len(ent)
                output.write("T{}\t{}\t{}\t{}\t{}\n".format( num, etype, start, end, ent ))
                etype = ""
                ent = ""
        elif line[4][0] == "B":
            num += 1
            etype = line[4].split('-')[1]#get entity type
            etype = etype.upper()#for uniformality
            etype = etype.strip('\n')#entity type has newline after it
            ent += line[0] + " " #get the entity
        else:
            ent+= line[0] + " " #get the rest of the entity
            

        line = fi.readline()

output.close()