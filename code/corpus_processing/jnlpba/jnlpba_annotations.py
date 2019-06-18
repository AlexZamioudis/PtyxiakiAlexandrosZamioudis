# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 22:33:25 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\jnlpba.txt"):
    os.remove("1. texts\\jnlpba.txt")

if os.path.exists("1. annotations\\jnlpba.txt"):
    os.remove("1. annotations\\jnlpba.txt")

output1 = open("1. texts\\jnlpba.txt", "a", encoding="utf8")
output2 = open("1. annotations\\jnlpba.txt", "a", encoding="utf8")

with open("jnlpba.iob2", encoding="utf8") as fi:  
    
   line = fi.readline()
   
   text = ""
   
   count = 0
   etype = "" #entity type
   ent = "" #entity
   start = 0 #entity start point
   end = 0 #entity end point
   
   num = 0
   while line:
        line = line.split('\t')
        
        if len(line) == 1:
            if count != 0 :#for the extra newlines
                output1.write("\n")#new line in the text
            line = fi.readline()
            count = 0
            continue #for the empty lines in the text
        else:#write the text
            text += line[0] + " "
            output1.write("{}".format(text))
            text = ""
        
        if line[1][0] == "O":
            if etype != "":
                end = start +len(ent) - 1 #minus 1 for the space after the last word
                output2.write("T{}\t{}\t{}\t{}\t{}\n".format( num, etype, start, end, ent ))
                etype = ""
                ent = ""
        elif line[1][0] == "B":
            num += 1
            etype = line[1].split('-')[1]#get entity type
            etype = etype.upper()#for uniformality
            etype = etype.strip('\n')#entity type has newline after it
            ent += line[0] + " " #get the entity
            start = count #where the entity starts, +1 for the 1st char
        else:
            ent+= line[0] + " " #get the rest of the entity
            
        count += len(line[0]) + 1 #+1 for the spaces

        line = fi.readline()

output1.close()     
output2.close()