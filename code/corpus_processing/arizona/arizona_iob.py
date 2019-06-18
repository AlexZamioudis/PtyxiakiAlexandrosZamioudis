# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 23:27:25 2019

@author: Αλέξανδρος
"""
import os 
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\arizona.iob2"):
    os.remove("1. iob\\arizona.iob2")

output = open("1. iob\\arizona.iob2", "a") #to be used as input for NER

def make_iob(txt, ents):
    """
    We split the text at the beginning of the entity and put
    an identifier, so after tokenization we know that the entity
    begins after the token position of the identifier
    """
    index = 0
    for i in ents:
        start = txt.index(i, index) #get the start of the entity
        tmp1, tmp2 = txt[:start], txt[start:]
        tmp1 += " eeeeeeeeeeeeeeeeeeee "
        txt = ' '.join([tmp1, tmp2])
        index = start + len(i) + len(" eeeeeeeeeeeeeeeeeeee ")
        
    line_tokens = word_tokenize(txt)#tokenize the text
    
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
            entity_iob = ['I-Disease'] * len(entity_tokens) #all entities in arizona are disease
            entity_iob[0] = "B-Disease"
                    
            #make changes to the iob tags to match the entities
            for j in range(0, len(entity_iob)):
                line_iob[starts[i] + j] = entity_iob[j]
            
        #the format is: token    IOB-Disease
        for i in range(0, len(line_tokens)):
            output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
        output.write('\n')#new document
    
def make_iob_nested(n):
    for i in range(0, len(n)):
        #tokenize the entities
        entity_tokens = word_tokenize(n[i])
        entity_iob = ['I-Disease'] * len(entity_tokens)  #all entities in arizona are disease
        entity_iob[0] = "B-Disease"
        
        for i in range(0, len(entity_tokens)):
            output.write("{}\t{}\n".format(entity_tokens[i], entity_iob[i]))
        output.write('\n')#new document

with open("arizona disease.txt") as fi:  
    
    line = fi.readline() #the 1st one is the types
    line = fi.readline()
    
    first_line = line.split('\t') # just for initialization
    text = first_line[3]
    entities = []
    prev_end = 0
    
    sentence_id = []
    sentence_id.append(first_line[0])
    
    while line:
        line = line.split('\t')
        
        sentence_id.append(line[0])
        
        if sentence_id[-1] != sentence_id[-2]: #the text changes per sentence_id
            
            """
            sort based on the start and reverse end in order to always 
            take the biggest entity
            """
            entities.sort(key=lambda x:(x[0],-x[1]))

            ents = []
            nested = []
            #find the nested entities
            for i in entities:
                if i[0] >= prev_end: #if start < previous and then it is a nested entity
                    ents.append(i[2])
                    prev_end = i[1]
                else:
                    nested.append(i[2])# dont update the end
                
            make_iob(text, ents) # make the iobs for the text
            
            """
            Because of nested entities we originaly print the text with 
            non nested entities and the we print seperatly the nested 
            entities in order to avoid duplicates of the O types
            """
            make_iob_nested(nested) 
            
            text = line[3]
            entities = []
            prev_end = 0
        
        if line[5] and line[5] != '0' and line[5] != line[4]: #if there are entities
            entities.append( [int(line[4]), int(line[5]), line[7]] ) #start end, and text

        line = fi.readline()

#print the last sentence_id
if sentence_id[-1] == sentence_id[-2]: #if it is the same sentence as the previous lines
    """
    sort based on the start and reverse end in order to always 
    take the biggest entity
    """
    entities.sort(key=lambda x:(x[0],-x[1]))

    ents = []
    nested = []
    #find the nested entities
    for i in entities:
        if i[0] >= prev_end: #if start < previous and then it is a nested entity
            ents.append(i[2])
            prev_end = i[1]
        else:
            nested.append(i[2])# dont update the end
        
    make_iob(text, ents) # make the iobs for the text
    
    """
    Because of nested entities we originaly print the text with 
    non nested entities and the we print seperatly the nested 
    entities in order to avoid duplicates of the O types
    """
    make_iob_nested(nested) 
else: #if it is just the last line
    ents = []
    if len(entities) == 1: #if the last line had an entity
        ents.append(entities[0][2])
    make_iob(text, ents) # make the iobs for the text
    
output.close()
