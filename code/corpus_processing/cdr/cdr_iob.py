# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 23:15:30 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\cdr.iob2"):
    os.remove("1. iob\\cdr.iob2")

output = open("1. iob\\cdr.iob2", "a", encoding="utf8")

with open("cdr.txt", encoding="utf8") as fi:  
   
    line = fi.readline()
    text = ""
    ents = []
    etypes = []
    cond = True
    while line:
        
        line = line.strip('\n')
        line = line.split('\t')
        
        if line[0] != '':#we dont want the empty lines
            if len(line) == 1: 
                cond = True
                line = line[0].split('|t|')#get the title
                if len(line) > 1:
                    text = line[1]
                else: #get the abstract
                    line = line[0].split('|a|')
                    text += " " + line[1] + "\n"
            elif len(line) > 4:  #the last line of every text is ids
                ents.append(line[3]) #get entities
                etypes.append(line[4])#get entity types
            elif cond: #make the iobs
                """
                We split the text at the beginning of the entity and put
                an identifier, so after tokenization we know that the entity
                begins after the token position of the identifier
                """
                cond = False
                index = 0
                for i in ents:
                    start = text.index(i, index) #get the start of the entity
                    index = start + len(i)
                    tmp1, tmp2 = text[:start], text[start:]
                    tmp1 += " eeeeeeeeeeeeeeeeeeee "
                    text = ' '.join([tmp1, tmp2])
                    
                    
                line_tokens = word_tokenize(text)#tokenize the text
                
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
                    tmp = 'I-'+etypes[i]
                    entity_iob = [tmp] * len(entity_tokens) #all entities in bc2 are genes/proteins
                    entity_iob[0] = "B-" + etypes[i]
                    
                    #make changes to the iob tags to match the entities
                    for j in range(0, len(entity_iob)):
                        line_iob[starts[i] + j] = entity_iob[j]
                        
                #the format is: token    IOB-etypes
                for i in range(0, len(line_tokens)):
                    output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
                
                output.write('\n')#new document
                
        else: # nullify for the next text
            ents = []
            etypes = []
        
        line = fi.readline()

output.close()