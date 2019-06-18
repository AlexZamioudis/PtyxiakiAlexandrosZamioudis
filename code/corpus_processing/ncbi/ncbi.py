# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 02:00:52 2019

@author: Αλέξανδρος
"""
import os
import re

if os.path.exists("1. texts\\ncbi.txt"):
    os.remove("1. texts\\ncbi.txt")

if os.path.exists("1. annotations\\ncbi.txt"):
    os.remove("1. annotations\\ncbi.txt")

output1 = open("1. texts\\ncbi.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\ncbi.txt", "a") #results in order to evaluate NER


with open("ncbi.txt", encoding="utf8") as fi:  
    line = fi.readline()
    num = 1
    while line:
        moved_text = 0 #since we remove tags from the text we need to keep the number of chars currently removed for correct starts and ends
        line = line.split("\t", 1)[1]#just remove the first word
        
        #get the annotations
        p = re.compile("<category=.*?>.+?</") #search for <category=ENTITY_TYPE>Entity</ENTITY_TYPE>
        for m in p.finditer(line):
            start = m.start() #The start of the entity
            end = m.end() - 2 - moved_text #The end of the entity, -2 for the "</" minus already removed text
            tag, text = m.group().split(">")#get Entity type and the entity
            start = start + len(tag) + 1 - moved_text#The entity starts after the type minus already removed text
            tag = tag[11:-1] #Entity type without "<category=" and " in the end
            text = text[:-2]#Entity without "</" in the end
            
            moved_text += 11 + len(tag) +14 #len of ( <category="tag"></category> )
            
            tag = "Disease" #all entity types are subgroups of the type disease
            output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, tag, start, end, text) )
            num += 1
        
        #get the text
        line = line.replace("</category>", "")
        line = re.sub('<category=.*?>', '', line)
        output1.write("{}".format(line))
        line = fi.readline()




output1.close()
output2.close()