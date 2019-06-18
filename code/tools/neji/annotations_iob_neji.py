# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 02:15:52 2019

@author: Αλέξανδρος
"""


import os
import json
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

def full_names(n):#get the full names of the entity types
    if n == "DISO":
        n = "disorder"
    elif n == "ANAT":
        n = "anatomy"
    elif n == "PRGE":
        n = "gene/protein"
    else:
        n = "unidentified" #in some cases no entity type is given
        
    return n

if os.path.exists("3. neji iob\\gpro.iob2"):
    os.remove("3. neji iob\\gpro.iob2")
    
output = open("3. neji iob\\gpro.iob2", "a", encoding="utf8")

with open("2. neji results\\gpro.json", encoding="utf8") as fi: 
    
    data = json.load(fi) #data is a list
    
    for i in data:#get the terms for each text
        text = i.get('text')
        terms = i.get('terms')
        
        ents = []
        etypes = []
        for j in terms:#get the annotations from the terms
            ent = j.get('ids') # get the entity type
            
            start = j.get('start')# get the start of the entity
            end = j.get('end')# get the end of the entity
            entity = j.get('text') #get the entity
            
            e_type = ""
            ent = ent.split('|') #check for multiple types for one entity
            s = set()
            for e in ent:
                e = e.split(':')[-1]#the enity type is in xxxx:xxxxxxxx:xxxx:entity_type
                e = full_names(e)
                s.add(e)
            
            for e in s:
                e_type += e + "/"
                
            e_type = e_type[:-1]#remove last /
            
            etypes.append(e_type)
            ents.append(entity)
        
        make_iob(text, ents, etypes)
    
output.close()