# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:31:49 2019

@author: Αλέξανδρος
"""

import os
import json

if os.path.exists("3. neji tags\\arizona.txt"):
    os.remove("3. neji tags\\arizona.txt")
    
output = open("3. neji tags\\arizona.txt", "a", encoding="utf8")

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

num = 0
with open("2. neji results\\arizona.json", encoding="utf8") as fi: 
    
    data = json.load(fi) #data is a list
    
    for i in data:#get the terms for each text
        terms = i.get('terms')
        
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
            
            num += 1   
            output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, e_type, start, end, entity))

    
    
    
output.close()