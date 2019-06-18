# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:57:02 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("3. abner tags\\scai_disease.txt"):
    os.remove("3. abner tags\\scai_disease.txt")

output = open("3. abner tags\\scai_disease.txt", "a", encoding="utf8")

with open("2. abner results\\scai_disease.sgml", encoding="utf8") as fi:  
    
    line = fi.readline()
    num = 0
    while line:
        index = 0 # where in the text are we
        moved_text = 0 #since we remove tags from the text we need to keep the number of chars currently removed for correct starts and ends

        end = line.find("</", index)#search for the </entity type>, we do that as a simply < or > might be part of the text
        while end != -1:
            e_type = line.find(">",end) #enitty type, search for the > in </entity type>
            e_type = line[end+2:e_type]# get the entity type in </entity type>
            
            start = line.rfind(">", index, end) + 2 #the start of the entity, plus 2 for the '> '
            index = end + len(e_type) + 3 #we are now in text after </entity type>
            end -= 1 #remove the space between entity and </
            
            ent = line[start:end] #the entity
            
            start = start - moved_text - len(e_type) - 3 #get the location in the non annotated text, aka current moved_text + <entity type>
            end = end - moved_text - len(e_type) - 3
            moved_text += 2*len(e_type) + 7 # we dont want to count "<entity type>  </entity type>"
            
            num += 1
            output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, e_type, start, end, ent) )
            
            end = line.find("</", index)

        line = fi.readline()
        
        
output.close()