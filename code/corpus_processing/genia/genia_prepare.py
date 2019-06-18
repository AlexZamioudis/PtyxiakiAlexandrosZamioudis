# -*- coding: utf-8 -*-
"""
Created on Sat Mar 9 21:29:19 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET


if os.path.exists("1. texts\\genia.txt"):
    os.remove("1. texts\\genia.txt")

if os.path.exists("1. annotations\\genia.txt"):
    os.remove("1. annotations\\genia.txt")

output1 = open("1. texts\\genia.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\genia.txt", "a") #results in order to evaluate NER

tree = ET.parse('genia.xml')
root = tree.getroot()

num = 0
#get the text
for r in root.iter('article'):
    index = 0 #at what char of the text we are, used for start and end of entities
    text = ''
    for i in r.itertext():
        if i is not None:  
            text = text + i
            
    text = ' '.join(text.split())#remove exces spaces
    text = text.split(' ',1)[1]#remove the id, it reduces score NER tools
    output1.write("{}\n".format(text))
    
    a_text = ''#annotation text
    a_type = ''#annotation type
    
    for i in r.iter('cons'): #find the annotations
        if i.text is not None: #normal case
            a_text = i.text #get the entity
            a_type = i.attrib.get('sem') # get the type
            start = text.find(a_text, index)#get the start of the entity
            end = text.find(a_text, index) + len(a_text)# the end of the entity
            
            num += 1
            output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, a_type, start, end, a_text)) 
            
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
            num += 1
            output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, a_type, start, end, a_text))          


output1.close()
output2.close()