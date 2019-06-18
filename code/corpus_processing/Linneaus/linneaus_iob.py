# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 17:13:56 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\linneaus.iob2"):
    os.remove("1. iob\\linneaus.iob2")

output = open("1. iob\\linneaus.iob2", "a", encoding="utf8")

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
            entity_iob = ["I-Species"] * len(entity_tokens)
            entity_iob[0] = "B-Species"
                    
            #make changes to the iob tags to match the entities
            for j in range(0, len(entity_iob)):
                line_iob[starts[i] + j] = entity_iob[j]
            
        #the format is: token    IOB-Species
        for i in range(0, len(line_tokens)):
            output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
        output.write('\n')#new document
    
def make_iob_nested(n):
    for i in range(0, len(n)):
        #tokenize the entities
        entity_tokens = word_tokenize(n[i])
        entity_iob = ["I-Species"] * len(entity_tokens)
        entity_iob[0] = "B-Species"
        
        #the format is: token    IOB-Species
        for i in range(0, len(entity_tokens)):
            output.write("{}\t{}\n".format(entity_tokens[i], entity_iob[i]))
        output.write('\n')#new document
        

#we save all the annotations and search for them in the text
annotations = []
ids = []
with open("linneaus.tsv", encoding="utf8") as fi:  
    
    line = fi.readline()
    line = fi.readline() #the first line is the column types
    
    while line:
        line = line.strip('\n')
        line = line.split("\t")
        
        line[4] = ' '.join(line[4].split()) #replace double spaces etc
        if len(line) != 1:
            annotations.append([ int(line[2]), int(line[3]), line[4]])
            ids.append(line[1])
        line = fi.readline()
 
dr = os.getcwd() + "\linneaus" #the folder with the files       
for filename in os.listdir(dr):
    
    name = filename[:-4] #the file name without .txt

    filename = dr + '\\' + filename #the actual path to file
    entities = []
    text = ""
    with open(filename, encoding="utf8") as fi:
        line = fi.readline()
        while line:
            line = line.replace('\n',' ') #remove the newlines
            text += line
            line = fi.readline()
            
        text = ' '.join(text.split())
        
        indices = [i for i, x in enumerate(ids) if x == name] #get the indexes of the entities
        
        for i in indices:
            entities.append(annotations[i])
        
        """
        due to the nested entities sometimes the order is broken
            
        sort based on the start and reverse end in order to always
        take the biggest entity
        """
        entities.sort(key=lambda x:(x[0],-x[1]))
        """
        Due to nested entities we print the nested entities seperate 
        from the rest of the text in order to dont have duplicates 
        of the Os
        """
        ents = []
        nested = []
        prev_end = 0
        #find the nested entities
        for i in entities:
            if i[0] >= prev_end: #if start < previous and then it is a nested entity
                ents.append(i[2])
                prev_end = i[1]
            else:
                nested.append(i[2])# dont update the end
        
        make_iob(text, ents)
        make_iob_nested(nested)

output.close()
