# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:50:37 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET

if os.path.exists("1. texts\\bioinfer.txt"):
    os.remove("1. texts\\bioinfer.txt")

if os.path.exists("1. annotations\\bioinfer.txt"):
    os.remove("1. annotations\\bioinfer.txt")

output1 = open("1. texts\\bioinfer.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\bioinfer.txt", "a") #results in order to evaluate NER

tree = ET.parse('bioinfer.xml')
root = tree.getroot()

num = 0

for i in root.iter('sentence'): #find the texts
    text = i.attrib.get("origText") #get the text
    output1.write("{}\n".format(text))  
    
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
        
        num += 1
        entity = entity[:-1] #minus one for the last space added
        end = int(start) + len(entity)
        
        output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, e_type, start, end, entity))


output1.close()
output2.close()