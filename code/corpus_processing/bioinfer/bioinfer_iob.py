# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 01:22:16 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET


if os.path.exists("1. iob\\bioinfer.iob2"):
    os.remove("1. iob\\bioinfer.iob2")

output = open("1. iob\\bioinfer.iob2", "a", encoding="utf8") #to be used as input for NER

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
    
def make_iob_nested(n, e):
    for i in range(0, len(n)):
        #tokenize the entities
        entity_tokens = word_tokenize(n[i])
        tmp = 'I-'+e[i]
        entity_iob = [tmp] * len(entity_tokens)
        entity_iob[0] = "B-" + e[i]
        
        #the format is: token    IOB-e
        for i in range(0, len(entity_tokens)):
            output.write("{}\t{}\n".format(entity_tokens[i], entity_iob[i]))
        output.write('\n')#new document


tree = ET.parse('bioinfer.xml')
root = tree.getroot()


for i in root.iter('sentence'): #find the texts
    text = i.attrib.get("origText") #get the text
    entities = []
    #make list of all the tokens, to be used to find the entities
    tokens_id = []
    tokens_start = []
    tokens_text = []
    for j in i.iter('token'):
        for k in j.iter('subtoken'):
            tokens_id.append(k.attrib.get('id'))
            tokens_start.append(j.attrib.get('charOffset'))
            tokens_text.append(k.attrib.get('text'))
    
    for j in i.iter('entity'):
        e_type = j.attrib.get('type')
        entity = ""
        start = 0
        for k in j.iter('nestedsubtoken'): #get the entity
            tmp = k.attrib.get('id')
            
            if entity == "": #get the start
                start = tokens_start[ tokens_id.index(tmp) ]
            
            entity += tokens_text[ tokens_id.index(tmp) ] + ' '
        
        entity = entity[:-1] #minus one for the last space added
        
        """
        The bioinfer corpus has entities that are not continuous in the text
        This entities are ignored as there is no way to turn them into iob format
        
        In the corpus the entities are sometimes written differently from 
        what they are in the text. Because this causes problems with
        word_tokenize we try to find in the text together with the start
        as due to this problem some entities are given similar starts
        while they are not similar
        """
        if entity != "": #deal with the case no entity is found
            try:# if its non continuous it will create an error
                tmp = text.index(entity, int(start))
                end = int(tmp) + len(entity)
                entities.append([ int(tmp), int(end), e_type, entity])
            except ValueError:
                pass
            
    """
    sort based on the start and reverse end in order to always take the 
    biggest entity
    """
    entities.sort(key=lambda x:(x[0],-x[1]))
    """
    Due to nested entities we print the nested entities seperate from
    the rest of the text in order to dont have duplicates of the Os
    """
    ents = []
    etypes = []
    nested = []
    nestedtypes = []
    prev_end = 0
    #find the nested entities
    for i in entities:
        if i[0] >= prev_end: #if start < previous and then it is a nested entity
            ents.append(i[3])
            etypes.append(i[2])
            prev_end = i[1]
        else:
            nested.append(i[3])# dont update the end
            nestedtypes.append(i[2])
    
    make_iob(text, ents, etypes)
    make_iob_nested(nested, nestedtypes)
        
output.close()