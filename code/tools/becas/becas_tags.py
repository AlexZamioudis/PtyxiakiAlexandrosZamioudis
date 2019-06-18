# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 00:52:50 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET

if os.path.exists("3. becas tags\\scai_disease.txt"):
    os.remove("3. becas tags\\scai_disease.txt")

output = open("3. becas tags\\scai_disease.txt", "a", encoding="utf-8") #to be used as input for NER

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

parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse('2. becas results\\scai_disease.xml', parser = parser)
root = tree.getroot()

num = 0
for r in root.iter('text'): #find the texts
    
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
        
        num += 1
        output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, entity_type, start, end, entity))

output.close()