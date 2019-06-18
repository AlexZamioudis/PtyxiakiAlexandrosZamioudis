# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 01:01:16 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\genia.iob2"):
    os.remove("1. iob\\genia.iob2")

output = open("1. iob\\genia.iob2", "a") 

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


tree = ET.parse('genia.xml')
root = tree.getroot()

#get the text
for r in root.iter('article'):
    entities = []
    index = 0 #at what char of the text we are, used for start and end of entities
    text = ''
    for i in r.itertext():
        if i is not None:
            text = text + i
            
    text = ' '.join(text.split())#remove exces spaces
    text = text.split(' ',1)[1]#remove the id, it reduces score NER tools
    
    a_text = ''#annotation text
    a_type = ''#annotation type
    
    for i in r.iter('cons'): #find the annotations
        if i.text is not None: #normal case
            a_text = i.text #get the entity
            a_type = i.attrib.get('sem') # get the type
            start = text.find(a_text, index)#get the start of the entity
            end = text.find(a_text, index) + len(a_text)# the end of the entity
            
            #check for empty entities
            if a_text != "" and a_text != None and a_text != "\n" and a_text != " ":
                #check if the entity exists correctly in the text
                try:
                    temp = text.index(a_text, start) 
                    
                    if a_type == None:
                        a_type = "Unknown"
                        
                    entities.append([int(start), int(end), a_type, a_text])
                    
                except ValueError:
                    pass
                
            index = end #we move the index of the text after the entity
            #output write etc
        else: #nested entities
            j = i[0]
            a_type = i.attrib.get('sem') #get the overall entity type
            if j.text is not None and j.tail is not None: #single nested
                # what we actually need is the tail,the text is another entity and will be found in the next iteration
                a_text = j.text + j.tail #the overall entity
            else: #multiple nested
                a_text = ''
                tmp = j
                #to get the text we need to go to the children
                while len(tmp) > 0:
                    tmp = tmp[0] #go to the child
                    if tmp.text is not None and tmp.tail is not None:
                        a_text += tmp.text + tmp.tail
                        
                if j.tail is not None:
                    a_text += j.tail  # add the tail as we did in single nested
            
            start = text.find(a_text, index)#get the start of the entity
            end = text.find(a_text,index) + len(a_text)
            """
            we do not update the index in nested entities, because we dont
            actually move in the text, we iterate over the whole entity for
            its nested entities
            """
            #check for empty entities
            if a_text != "" and a_text != None and a_text != "\n" and a_text != " ":
                #check if the entity exists correctly in the text
                try:
                    temp = text.index(a_text, start) 
                    
                    if a_type == None:
                        a_type = "Unknown"
                        
                    entities.append([int(start), int(end), a_type, a_text])
                    
                except ValueError:
                    pass
    
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