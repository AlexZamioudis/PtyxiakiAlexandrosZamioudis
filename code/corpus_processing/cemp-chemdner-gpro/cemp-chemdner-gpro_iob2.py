# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:52:44 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob1\\gpro.iob2"):
    os.remove("1. iob1\\gpro.iob2")

output = open("1. iob1\\gpro.iob2", "a", encoding="utf8")


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

#we save all the annotations and search for them in the text
annotations = []
ids = []
with open("gpro.tsv", encoding="utf8") as fi:  
    
    line = fi.readline()
    
    while line:
        line = line.strip('\n')
        line = line.split("\t")
        
        if len(line) != 1:
            annotations.append(line[1:])
            ids.append(line[0])
        line = fi.readline()
        
with open("gpro.txt", encoding="utf8") as fi:  
    
    line = fi.readline()
    while line:
        entities = []
        line_id, line_text = line.split(None, 1)#get the first word(id) and the text
        title_end = line_text.index('\t') #get the length of the title in order to get the correct starts
        line_text = line_text.strip('\t')
        line_text = line_text.strip('\n')
        
        indices = [i for i, x in enumerate(ids) if x == line_id] #get the indexes of the entities
        
        for i in indices:#get the entities
            if annotations[i][0] == "A": # correct the starts by counting the title
                annotations[i][1] = int(annotations[i][1]) + title_end
                annotations[i][2] = int(annotations[i][2]) + title_end
            entities.append([int(annotations[i][1]), int(annotations[i][2]), annotations[i][4], annotations[i][3]])
        
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
        
        make_iob(line_text, ents, etypes)
        make_iob_nested(nested, nestedtypes)
        
        line = fi.readline()
        
        
output.close()