# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 01:22:56 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\s800.iob2"):
    os.remove("1. iob\\s800.iob2")

output = open("1. iob\\s800.iob2", "a", encoding="utf8")

#get annotations
ents = []#entities
with open("s800.tsv", encoding="utf8") as fi:  
    
   line = fi.readline()

   while line:
        line = line.split('\t')
        
        file_num = line[1].split(':')[0] # get speciesfilenum from speciesfilenum:xxxxxxxx
        file_num = file_num[7:]# get filenum from speciesfilenum
        ents.append([file_num, line[4].strip('\n')])
                
        line = fi.readline()

#get text
dr = os.getcwd() + "\s800" #the folder with the files

for filename in os.listdir(dr):
    num = filename[7:-4] #the file number
    
    filename = dr + '\\' + filename #the actual path to file
    
    text = ""
    with open(filename, encoding="utf8") as fi:
        line = fi.readline()
        while line:
            line = line.replace('\n',' ') #remove the newlines
            text += line
            line = fi.readline()
            
        text = ' '.join(text.split())
        entities = [e[1] for e in ents if e[0] == num]
        
        
    """
    As the beginning word of the entity can be multiple times in the
    text, we split the text at the beginning of the entity and put
    an identifier, so after tokenization we know that the entity
    begins after the token position of the identifier
    """
    
    index = 0
    for i in entities:
        start = text.index(i, index) #get the start of the entity
        tmp1, tmp2 = text[:start], text[start:]
        tmp1 += " eeeeeeeeeeeeeeeeeeee "
        text = ' '.join([tmp1, tmp2])
        index = start + len(i) + len(" eeeeeeeeeeeeeeeeeeee ")
    
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
    
    for i in range(0, len(entities)):
        #tokenize the entities
        entity_tokens = word_tokenize(entities[i])
        entity_iob = ['I-Species'] * len(entity_tokens) #all entities in bc2 are genes/proteins
        entity_iob[0] = "B-Species"
            
        #make changes to the iob tags to match the entities
        for j in range(0, len(entity_iob)):
            line_iob[starts[i] + j] = entity_iob[j]
        
        
    #the format is: token    IOB-PROTEIN
    for i in range(0, len(line_tokens)):
        output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
    output.write('\n')#new document
    
output.close()