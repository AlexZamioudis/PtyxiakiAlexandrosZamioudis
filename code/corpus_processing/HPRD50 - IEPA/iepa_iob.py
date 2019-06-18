# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 00:06:16 2019

@author: Αλέξανδρος
"""
import os 
from nltk.tokenize import word_tokenize
import xml.etree.ElementTree as ET

if os.path.exists("1. iob\\iepa.iob2"):
    os.remove("1. iob\\iepa.iob2")
    
output = open("1. iob\\iepa.iob2", "a", encoding="utf8")


tree = ET.parse('iepa.xml')
root = tree.getroot()


for r in root.iter('passage'): #find the texts
    ents = []
    j = r.find('text')
    text = j.text
    text = ' '.join(text.split()) #remove newlines and tabs from the text
    
    for k in r.iter('annotation'):
        entity = k.find('text').text
        start = k.find('location').get('offset')
        ents.append([int(start), entity]) #start needs to be int for correct sorting
    
    #the entities are given in random order, we need them sorted for the iob format to be made
    ents.sort()
    ents = [row[1] for row in ents]

    
    """
    As the beginning word of the entity can be multiple times in the
    text, we split the text at the beginning of the entity and put
    an identifier, so after tokenization we know that the entity
    begins after the token position of the identifier
    """
    
    index = 0
    for i in ents:
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
    
    for i in range(0, len(ents)):
        #tokenize the entities
        entity_tokens = word_tokenize(ents[i])
        entity_iob = ['I-PROTEIN'] * len(entity_tokens) #all entities in bc2 are genes/proteins
        entity_iob[0] = "B-PROTEIN"
            
        #make changes to the iob tags to match the entities
        for j in range(0, len(entity_iob)):
            line_iob[starts[i] + j] = entity_iob[j]
        
        
    #the format is: token    IOB-PROTEIN
    for i in range(0, len(line_tokens)):
        output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
    output.write('\n')#new document
    

output.close()