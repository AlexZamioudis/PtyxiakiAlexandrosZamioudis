# -*- coding: utf-8 -*-
"""
Created on Tue May 21 22:43:01 2019

@author: Αλέξανδρος
"""


import os
import re
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\ncbi.iob2"):
    os.remove("1. iob\\ncbi.iob2")

output = open("1. iob\\ncbi.iob2", "a", encoding="utf8")

with open("ncbi.txt", encoding="utf8") as fi:  
    line = fi.readline()
    
    while line:
        ents = []
        
        moved_text = 0 #since we remove tags from the text we need to keep the number of chars currently removed for correct starts and ends
        line = line.split("\t", 1)[1]#just remove the first word
        
        #get the annotations
        p = re.compile("<category=.*?>.+?</") #search for <category=ENTITY_TYPE>Entity</ENTITY_TYPE>
        for m in p.finditer(line):
            text = m.group().split(">")[1]#get the entity
            text = text[:-2]#Entity without "</" in the end
            
            ents.append(text)
        
        #get the text
        line = line.replace("</category>", "")
        line = re.sub('<category=.*?>', " eeeeeeeeeeeeeeeeeeee ", line)
        
        #make the IOBs
        line_tokens = word_tokenize(line)#tokenize the text
        
        #get the starting positions of the entities
        starts = []
        try: #in order to handle the last case where list.index doesnt finds anything
            while line_tokens.index("eeeeeeeeeeeeeeeeeeee") > -1:
                tmp = line_tokens.index("eeeeeeeeeeeeeeeeeeee")
                starts.append(tmp)
                del line_tokens[tmp]
        except ValueError:
            pass
        
        line_iob = ['O'] * len(line_tokens)# the iob tags of the whole text
        
        for i in range(0, len(ents)):
            #tokenize the entities
            entity_tokens = word_tokenize(ents[i])
            tmp = "I-Disease"
            entity_iob = [tmp] * len(entity_tokens) #all entities in bc2 are genes/proteins
            entity_iob[0] = "B-Disease"
                    
            #make changes to the iob tags to match the entities
            for j in range(0, len(entity_iob)):
                line_iob[starts[i] + j] = entity_iob[j]
            
        #the format is: token    IOB-etype
        for i in range(0, len(line_tokens)):
            output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
        output.write('\n')#new document
        
        line = fi.readline()




output.close()