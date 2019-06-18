# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:34:44 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

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

if os.path.exists("3. calais iob\\scai_disease.iob2"):
    os.remove("3. calais iob\\scai_disease.iob2")
    
output = open("3. calais iob\\scai_disease.iob2", "a", encoding="utf8")

dr = os.getcwd() + "\calais_out\\scai_disease" #the folder with the files

for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    e_type = "" #entity type
    #some times the same entity is found multiple times,
    #so we get the previous entity type

    with open(filename, encoding="utf-8") as fi:
        
        line = fi.readline()
        
        while line:
            text_start = line.find('document":"') + len('document":"')#where the text starts
            text_end = line.find('","docTitle"') #where the text ends
            text = line[text_start:text_end] 
            text = text.strip("\\n") #remove newlines
            
            entities = []
            
            line = line.split('exact":"') #find the entities in "exact":"entity"
            for i in range(1,len(line)):
                entity = line [i] [ 0 : line[i].find('"') ] #get the entity
                
                #get the start of the entity, its in "offset":start,"length"
                start = line [i] [ ( line[i].find('"offset":') + 9) : line[i].find(',"length"') ] 
                
                end = int(start) + len(entity) #the end of the entity
                
                ent = line[i-1] #find the entity type in "_type":"entity type"
                ent = ent.split('_type":"')
                
                if len(ent) > 1:#get the entity
                    e_type = ent[1][ 0 : ent[1].find('"') ]
                
                if entity in text: #check if the found entity exist in this form in the text
                    entities.append([int(start), int(end), e_type, entity])

            
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
            
            line = fi.readline()
              
output.close()