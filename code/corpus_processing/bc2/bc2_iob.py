# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 00:52:21 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\bc2.iob2"):
    os.remove("1. iob\\bc2.iob2")

output = open("1. iob\\bc2.iob2", "a", encoding="utf8")

nesid = [] #named entities id
nes = []#named entities

#get the entities and put them in a list for easier identification
with open("GENE.eval", encoding="utf8") as fi:  
    
    line = fi.readline()
   
    while line:
        line = line.split("|")
        nesid.append(line[0])
        nes.append(line[2])
               
        line = fi.readline()


with open("test.in", encoding="utf8") as fi:  
    
    line = fi.readline()
   
    while line:
        line_id, line_text = line.split(None, 1)#get the first word(id) and the text
        
        ents = [] #the entities for the current line
        indices = [i for i, x in enumerate(nesid) if x == line_id] #get the indexes of the entities
        
        for i in indices:#get the entities
            tmp = nes[i]
            tmp = tmp.strip('\n') #remove newlines
            ents.append(tmp)
        
        """
        We split the text at the beginning of the entity and put
        an identifier, so after tokenization we know that the entity
        begins after the token position of the identifier
        """
        index = 0
        for i in ents:
            start = line_text.index(i, index) #get the start of the entity
            tmp1, tmp2 = line_text[:start], line_text[start:]
            tmp1 += " eeeeeeeeeeeeeeeeeeee "
            line_text = ' '.join([tmp1, tmp2])
            index = start
        
        line_tokens = word_tokenize(line_text)#tokenize the text
        
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
            entity_iob = ['I-GENES/PROTEINS'] * len(entity_tokens) #all entities in bc2 are genes/proteins
            entity_iob[0] = "B-GENES/PROTEINS"
            
            #make changes to the iob tags to match the entities
            for j in range(0, len(entity_iob)):
                line_iob[starts[i] + j] = entity_iob[j]
        
        
        #the format is: token    IOB-PROTEINS
        for i in range(0, len(line_tokens)):
            output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
        
        output.write('\n')#new document
        line = fi.readline()
    
output.close()