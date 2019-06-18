# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 20:00:16 2019

@author: Αλέξανδρος
"""


import os

def find_starts(text, entities):
    index = 0
    starts = []
    for i in entities:
        pos = text.find(i, index)
        if pos != -1:
            index = pos + len(i)
            tmp = text[:pos]
            wsb = len(tmp) - len(tmp.replace(" ", "")) #white spaces between the words
            """
            In the biocreative corpus the starts of the entities are given without
            counting the whitespaces
            """
            starts.append(pos - wsb)
        else:
            starts.append(-1)
        
    return starts

dr = os.getcwd() + "\\1. iob2" #the folder with the files

for filename in os.listdir(dr):
    name = filename[:-5]
    
    print(name) #to check progress

    filename = dr + '\\' + filename #the actual path to file
    
    if os.path.exists("1. bc2 texts\\" + name + ".txt"):
        os.remove("1. bc2 texts\\" + name + ".txt")
    
    if os.path.exists("1. bc2 annotations 2\\" + name + ".ann"):
        os.remove("1. bc2 annotations 2\\" + name + ".ann")
    
    output1 = open("1. bc2 texts\\" + name + ".txt", "a", encoding="ascii")
    output2 = open("1. bc2 annotations 2\\" + name + ".ann", "a", encoding="ascii")
    
    
    with open(filename, encoding="utf8") as fi:      
        line = fi.readline()
       
        text = ""
        cond = True
        prev = 0
        
        entities = []
        etypes = []
        count = 0
        ent = "" #entity
        etype = "" #entity type
       
        num = 0
        while line:
            line = line.split('\t')
            
            if len(line) == 1:     
                if len(text) > 0:
                    if text[-1] == " ":
                        text = text[:-1]
                output1.write("{}\n".format(text))
                starts = find_starts(text, entities)
                
                for i in range(0 , len(starts)):
                    if starts[i] != -1:
                        # in the biocreative corpus the entities are given smaller end than the actual one
                        end = starts[i] + len(entities[i].replace(" ", "")) - 1 #dont count whitespaces
                        output2.write("SENTENCE{}|{}|{} {}|{}\n".format(num, etypes[i], starts[i], end,  entities[i] ))
                
                text = ""
                entities = []
                etypes = []
                line = fi.readline()
                cond = True
                continue #for the empty lines in the text
            else:#write the text
                if cond == True:#write sentence_id in the beginning of the text
                    num += 1
                    output1.write("SENTENCE{} ".format(num))
                    cond = False
                text += line[0] + " "
            
            if line[1][0] == "O":
                prev = "O"
                if ent != "": #the entity has ended, write it to file
                    ent = ent[:-1] #minus 1 for the space after the last word
                    entities.append(ent)
                    etypes.append(etype)
                    ent = ""
                    etype = ""
            elif line[1][0] == "B":
                if prev == "I":#in case an entity is immediatly followed by another entity
                    if ent != "":
                        ent = ent[:-1] #minus 1 for the space after the last word
                        entities.append(ent)
                        etypes.append(etype)
                        ent = ""
                        etype = ""
                prev = "B"
                etype = line[1][2:] #the type is line[1] without 'B-'
                etype = etype.strip('\n')
                
                ent+= line[0] + " " #get the entity
            else:
                prev = "I"
                ent+= line[0] + " " #get the entity
    
            line = fi.readline()
    
    #since we write to file only when we encounter an empty line, check if we wrote the last sentence
    if text != "" and len(entities) > 0: #write the last sentence
        if len(text) > 0:
            if text[-1] == " ":
                text = text[:-1]
        output1.write("{}\n".format(text))
        starts = find_starts(text, entities)
        
        for i in range(0 , len(starts)):
            if starts[i] != -1:
                # in the biocreative corpus the entities are given smaller end than the actual one
                end = starts[i] + len(entities[i].replace(" ", "")) - 1 #dont count whitespaces
                output2.write("SENTENCE{}|{} {}|{}\n".format(num, starts[i], end,  entities[i] ))
        
    output1.close()     
    output2.close()