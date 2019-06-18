# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:29:33 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

dr = os.getcwd() + "\\2. abner results trained" #the folder with the files

for filename in os.listdir(dr):
    name = filename[:-5]
    
    print(name) #to check progress
    
    name = name + ".iob2"

    if os.path.exists("3. abner iob trained\\" + name):
        os.remove("3. abner iob trained\\" + name)
    
    output = open("3. abner iob trained\\" + name, "a", encoding="utf8")
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:  
        
        line = fi.readline()
        while line:
            ents = []
            etypes = []
            
            index = 0 # where in the text are we
            moved_text = 0 #since we remove tags from the text we need to keep the number of chars currently removed for correct starts and ends
    
            end = line.find("</", index)#search for the </entity type>, we do that as a simply < or > might be part of the text
            while end != -1:
                endpoint = line.find(">",end) #search for the enity type by searching > in </entity type>
                e_type = line[end+2:endpoint]# get the entity type in </entity type>
                
                start = line.rfind("<" + e_type + ">", index, end) + len("<" + e_type + ">") + 1 #the start of the entity, plus 1 for the '<entity_type> '
                startpoint = start - 3 - len(e_type) # the enity begins in index <entity type>
                end -= 1 #remove the space between entity and </
                ent = line[start:end] #the entity
                
                line = line[:end] + line[endpoint + 1:] # we delete </entity type>
                line = line[:startpoint] + " eeeeeeeeeeeeeeeeeeee " + line[start:] #we replace <entity type> with the identifier
                """
                we turned '<entity type> ent </entity type>' 
                to ' eeeeeeeeeeeeeeeeeeee ent' the begining of which is the
                startpoint. So the new index is after the ent
                """
                index = startpoint + len(" eeeeeeeeeeeeeeeeeeee ") + len(ent)
                
                ents.append(ent)
                etypes.append(e_type)
    
                end = line.find("</", index)
            """
            We split the text at the beginning of the entity and put
            an identifier, so after tokenization we know that the entity
            begins after the token position of the identifier
            """
            #make the IOBs
            line_tokens = word_tokenize(line)#tokenize the text
                
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
                tmp = "I-" + etypes[i]
                entity_iob = [tmp] * len(entity_tokens) #all entities in bc2 are genes/proteins
                entity_iob[0] = "B-" + etypes[i]
                
                #make changes to the iob tags to match the entities
                for j in range(0, len(entity_iob)):
                    line_iob[starts[i] + j] = entity_iob[j]
                
            #the format is: token    IOB-etype
            for i in range(0, len(line_tokens)):
                output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
            output.write('\n')#new document
    
            line = fi.readline()
            
            
    output.close()