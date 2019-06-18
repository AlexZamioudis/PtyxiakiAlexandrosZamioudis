# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 01:59:12 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize

def full_names(n):
    if n == "SPEC":
        n = "species"
    elif n == "ANAT":
        n = "anatomy"
    elif n == "DISO":
        n = "disorder"
    elif n == "PATH":
        n = "pathway"
    elif n == "CHED":
        n = "chemical"
    elif n == "ENZY":
        n = "enzyme"
    elif n == "MRNA":
        n = "miRNA"
    elif n == "PRGE":
        n = "gene/protein"
    elif n == "COMP":
        n = "cellular_component"
    elif n == "FUNC":
        n = "molecular_function"
    elif n == "PROC":
        n = "biological_process"
        
    return n

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


if os.path.exists("3. becas iob\\scai_disease.iob2"):
    os.remove("3. becas iob\\scai_disease.iob2")

output = open("3. becas iob\\scai_disease.iob2", "a", encoding="utf-8") #to be used as input for NER


parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse('2. becas results\\scai_disease.xml', parser = parser)
root = tree.getroot()

for r in root.iter('text'): #find the texts
    
    entities = []
    
    index = 0 #at what char of the text we are, used for start and end of entities
    text = '' #the  text, used to find start and end of entities
    for i in r.itertext():
        if i is not None:  
            text = text + i
            
    text = ' '.join(text.split())#remove exces spaces
    
    #find the entities
    for i in r.iter('e'):
        
        if i.text is None: #if it is no a single entity it will consist of words
            entity = ""
            entity_type = ""
            
            #######IMPORTANT#######
            #on nested entities, becas doesnt specify what type the overall entity is
            #instead it gives a type to every token of it
            #as such we give the overall entity all the types of its tokens
            
            e_type = i.attrib.get('id')#the type is the last part of the id
            e_type = e_type.split("|")#the entity has multiple types
            
            for z in e_type:
                z = z.split(":")[3]
                z = z.strip(")")
                z = z.strip("(")
                z = full_names(z) # get full name
                entity_type += z +"/"
            
            entity_type = entity_type[:-1]#remove the last /
            
            for j in i.iter('w'):
                #special cases for punctupunctuation in the entities
                #if it is not done, it messes up with start and end
                if j.text[0] == '-' or j.text[0] == '/':
                    entity = entity[:-1]
                    entity += j.text
                elif j.text[0] == '\'' or j.text[0] == ')':
                    entity = entity[:-1]
                    entity += j.text + " "
                elif j.text[0] == '(' :
                    entity += j.text
                else:
                    entity += j.text + " "
        else:
            entity_type = ""
            entity = i.text
            e_type = i.attrib.get('id')#the type is the last part of the id
            e_type = e_type.split("|")#some entities have multiple types
            if len(e_type) > 1:#get multiple types
                for z in e_type:
                    z = z.split(":")[3]
                    z = full_names(z) # get full name
                    entity_type += z +"/"
            else:#get single type
                e_type = e_type[0]
                e_type = e_type.split(":")[3]
                e_type = full_names(e_type) # get full name
                entity_type = e_type
        
        
        #remove excess spaces for correct end
        if entity[-1] == ' ':
            entity = entity[:-1]
        
        #clear the entity types from duplicate entries and other leftovers
        if entity_type[-1] == ' ' or entity_type[-1] == "/":
            entity_type = entity_type[:-1]
        
        tmp = set()
        for z in entity_type.split('/'):
            if z not in tmp:
                tmp.add(z)
                
        entity_type = ""
        for z in tmp:
            entity_type += z + "/"
        entity_type = entity_type[:-1]
        
        start = text.find(entity, index)
        end = start + len(entity)
        index = end #update index to avoid constantly locating the 1st mention
        
        entities.append([start, end, entity_type, entity])
    """
    due to the nested entities sometimes the order is broken
    
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