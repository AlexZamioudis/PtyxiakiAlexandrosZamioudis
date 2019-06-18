# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 01:11:24 2019

@author: Αλέξανδρος
"""

import os
from nltk.tokenize import word_tokenize

if os.path.exists("1. iob\\osiris.iob2"):
    os.remove("1. iob\\osiris.iob2")

output = open("1. iob\\osiris.iob2", "a", encoding="utf8")
dr = os.getcwd() + "\osiris" #the folder with the files

t = 0
for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    if '.ann' not in filename: #do not open files with annotations
        with open(filename, encoding="utf8") as fi:
        
            line = fi.readline()
            num = 0
            id_len = 0 #the given indexes count the file id
            title_len = 0 #we put title and text in same row, we need to update start and for the \n
            text = "" #the text is in th
            while line:
                num += 1
                
                #dont get id in text, it reduces score of NER tools
                if num == 1 :
                    id_len = len(line) + 1 #get length of id, +1 for empty line2
                elif num == 3:
                    title_len = len(line)#we remove 1 newline but add 1 space so no need for change
                    line = line.strip()
                    text = text + line + " " # so that "title. Text"
                else: 
                    line = line.strip()
                    text = text + line #put title and text to same row
                    
                line = fi.readline()
            
            ents = []
            #open the annotations
            #the annotations dont contain the NE, only its location
            with open(filename + '.ann', encoding="utf8") as fi:  
                        
                line = fi.readline()
                       
                while line:
                           
                    if "type=\"ge\"" in line: #get only the gene annotations
                        t += 1
                        start, end = line.split('..') # split span="start..end"
                        start = start.split('span=\"')[1] # get start
                        end = end.split('\"')[0] # get end
                        start = int(start) - id_len
                        end = int(end) - id_len
                        if start > title_len: #after the title there is one additional char for empty line4
                            start -= 1
                            end -= 1
                            
                        ents.append(text[int(start):int(end)])
                    line = fi.readline()
                    
            """
            We split the text at the beginning of the entity and put
            an identifier, so after tokenization we know that the entity
            begins after the token position of the identifier
            """
            index = 0
            for i in ents:
                start = text.index(i, index) #get the start of the entity
                tmp1, tmp2 = text[:start], text[start:]
                tmp1 += " eeeeeeeeeeeeeeeeeeee "
                text = ' '.join([tmp1, tmp2])
                index = start + len(i)

            
            line_tokens = word_tokenize(text)#tokenize the text
                
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
                entity_iob = ['I-Gene'] * len(entity_tokens) #all entities in bc2 are genes/proteins
                entity_iob[0] = "B-Gene"
                    
                #make changes to the iob tags to match the entities
                for j in range(0, len(entity_iob)):
                    line_iob[starts[i] + j] = entity_iob[j]
            
            #the format is: token    IOB-Gene
            for i in range(0, len(line_tokens)):
                output.write("{}\t{}\n".format(line_tokens[i], line_iob[i]))
            output.write('\n')#new document

output.close()