# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 21:03:19 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

def make_iob(txt, ents, etypes):
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
            tmp = 'I-'+etypes[i]
            entity_iob = [tmp] * len(entity_tokens)
            entity_iob[0] = "B-" + etypes[i]
                    
            #make changes to the iob tags to match the entities
            for j in range(0, len(entity_iob)):
                line_iob[starts[i] + j] = entity_iob[j]
            
        #the format is: token    IOB-etypes
        for i in range(0, len(line_tokens)):
            output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
        output.write('\n')#new document

files = ["arizona", "bc2", "bioinfer", "cdr", "cellfinder", "cemp", "chemdner", "deca",
"genia", "gpro", "hprd50", "iepa", "jnlpba", "linneaus", "loctext", "ncbi", "osiris",
"s800", "scai_chemicals", "scai_disease"]

for name in files:
    print(name)#just to check progress

    if os.path.exists("1. train iob\\" + name + ".iob2"):
        os.remove("1. train iob\\" + name + ".iob2")
    
    output = open("1. train iob\\" + name + ".iob2", "a", encoding="utf8")
    
    nesid = [] #named entities id
    ne = [] #name entities
    
    #get the entities and put them in a list for easier identification
    with open("1. train test 2\\" + name + "_train.ann", encoding="utf8") as fi:  
        
        line = fi.readline()
       
        while line:
            line = line.split("|")
            if len(line)>1:
                nesid.append(line[0])
                start, end = line[2].split(' ')
                ne.append([int(start), int(end), line[1], line[3].strip('\n')]) #start, end, etype, entity
                   
            line = fi.readline()
    
    
    with open("1. train test 2\\" + name + "_train.txt", encoding="utf8") as fi:  
        
        line = fi.readline()
       
        while line:
            line_id, line_text = line.split(None, 1)#get the first word(id) and the text
            
            entities = []
            indices = [i for i, x in enumerate(nesid) if x == line_id] #get the indexes of the entities
            
            for i in indices:#get the entities
                entities.append(ne[i])
            """
            sometimes the order is broken
            
            sort based on the start and reverse end in order to always take the 
            biggest entity
            """
            entities.sort(key=lambda x:(x[0],-x[1]))
            
            ents = []
            etypes = []
            #find the nested entities
            for i in entities:
                ents.append(i[3])
                etypes.append(i[2])
            
            make_iob(line_text, ents, etypes)
            
            line = fi.readline()
        
    output.close()