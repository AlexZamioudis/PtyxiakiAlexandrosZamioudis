# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 01:44:46 2019

@author: Αλέξανδρος
"""

import os
import json
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\loctext.iob2"):
    os.remove("1. iob\\loctext.iob2")

output = open("1. iob\\loctext.iob2", "a", encoding="utf8")

dr = os.getcwd() + "\LocText" #the folder with the files

for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:
        data = json.load(fi)

        text = data.get("text")
        text = text.replace('\n',' ')#remove newline from text
                
        annotations = data.get("denotations")# get annotations
        
        if annotations: #in case it doesnt have any annotations
            start = 0
            end = 0
            ents = []
            prev = 0 #in some cases the same entity is given more than one times
            for i in annotations:
                span = i.get("span")
                start = span.get("begin")
                end = span.get("end")
                
                if start != prev:
                    ents.append(text[start:end])
                    prev = start
                
                
            """
            We split the text at the beginning of the entity and put
            an identifier, so after tokenization we know that the entity
            begins after the token position of the identifier
            """
            index = 0
            for i in ents:
                start = text.index(i, index) #get the start of the entity
                tmp1, tmp2 = text[:start], text[start:]
                tmp1 += " eeeeeeeeeeeeeeeeeeee "
                text = ' '.join([tmp1, tmp2])
                index = start + len(i)

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
                entity_iob = ['I-Gene/Protein'] * len(entity_tokens) #all entities in bc2 are genes/proteins
                entity_iob[0] = "B-Gene/Protein"
                    
                #make changes to the iob tags to match the entities
                for j in range(0, len(entity_iob)):
                    line_iob[starts[i] + j] = entity_iob[j]
            
            #the format is: token    IOB-Genes/Proteins
            for i in range(0, len(line_tokens)):
                output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
            output.write('\n')#new document
            
            
          
output.close()