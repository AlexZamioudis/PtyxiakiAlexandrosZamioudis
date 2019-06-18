# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 02:00:28 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\cellfinder.iob2"):
    os.remove("1. iob\\cellfinder.iob2")

output = open("1. iob\\cellfinder.iob2", "a", encoding="utf8")


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


dr = os.getcwd() + "\cellfinder_corpus" #the folder with the files

entities = []
for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    """
    The corpus folder format is filename.ann with the annotations
    and filename.txt with the text
    """
    if '.ann' in filename: #open the file with the annotations
        with open(filename, encoding="utf8") as fi:
        
            line = fi.readline()
            
            while line:
                line = line.split(None, 4) #dont split the text
                
                entities.append([ int(line[2]), int(line[3]), line[1], line[4].strip('\n')])
                
                line = fi.readline()
            
    else:#open the text
        with open(filename, encoding="utf8") as fi:
        
            line = fi.readline()
            text = ""
            while line:
                line = line.strip('\n')
                
                text += line + " "
                
                line = fi.readline()
            
            text = text[:-1] #remove last space
        
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
        
        entities = [] #empty the entities for the next file of annotations
output.close()