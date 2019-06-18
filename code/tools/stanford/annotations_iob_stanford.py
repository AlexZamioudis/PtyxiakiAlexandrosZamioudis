# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 23:19:15 2019

@author: Αλέξανδρος
"""

"""
IMPORTANT

Although the stanford results are almost identical to the ones of abner, with 
just less spaces inbetween the annotaions, the process crashes due to
Ram overload for some reason. As such a different process is followed
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
        

if os.path.exists("3. stanford iob trained\\cellfinder.iob2"):
    os.remove("3. stanford iob trained\\cellfinder.iob2")

output = open("3. stanford iob trained\\cellfinder.iob2", "a", encoding="utf8")

with open("2. stanford results trained\\cellfinder.sgml", encoding="utf8") as fi:  
    
    line = fi.readline()
    while line:
        ents = []
        etypes = []
        etypes_set = set()
        index = 0 # where in the text are we
        moved_text = 0 #since we remove tags from the text we need to keep the number of chars currently removed for correct starts and ends
        
        line = line.replace("</=", "")#necessary in some corpuses in order for program to work
        
        end = line.find("</", index)#search for the </entity type>, we do that as a simply < or > might be part of the text
        while end != -1:
            e_type = line.find(">",end) #entity type, search for the > in </entity type>
            e_type = line[end+2:e_type]# get the entity type in </entity type>
            
            start = line.rfind(">", index, end) + 1 #the start of the entity, plus 1 for the '>'
            index = end + len(e_type) + 3 #we are now in text after </entity type>
            
            ent = line[start:end] #the entity

            ents.append(ent)
            etypes.append(e_type)
            etypes_set.add(e_type)
            
            end = line.find("</", index)
            
        for i in etypes_set: # remove the <entity type> and </entity type> from the text
            line = line.replace('<' + i + '>', "")
            line = line.replace('</' + i + '>', "")
            
        make_iob(line, ents, etypes)
        
        line = fi.readline()
        
output.close()
