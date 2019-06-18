# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 00:09:14 2019

@author: Αλέξανδρος
"""
import os

"""
The purpose of this program is to break the iob texts in sentences
and remove non ascii characters
"""

dr = os.getcwd() + "\\1. iob1" #the folder with the files

for filename in os.listdir(dr):
    name = filename
    
    print(name) #to check progress

    filename = dr + '\\' + filename #the actual path to file
    
    if os.path.exists("1. iob2\\" + name):
        os.remove("1. iob2\\" + name)
    
    output = open("1. iob2\\" + name, "a", encoding="ascii")
    
    with open(filename, encoding="utf8") as fi:      
        line = fi.readline()
        
        first_line = line.split('\t')
        prev_text = first_line[0] #for initialization

        while line:
            tmp_line = ""
            
            for i in line: #replace non ascii characters with #
                if ord(i) < 128:
                    if i == "|":
                        tmp_line += "#"
                    else:
                        tmp_line += i
                else:
                    tmp_line += "#"
                    
            line = tmp_line
            
            line1 = line.split('\t')
            
            if len(line1) == 1: #empty line
                output.write("\n") # new sentence
            else:
                text = line1[0]
                typ = line1[1][0]# the IOB type
                
                line1[1] = line1[1].replace(" ","")#remove space from entity type
                line = line1[0] + '\t' + line1[1]
                
                if len(prev_text) > 0:
                    if prev_text == '.' or prev_text[-1] == '.' or prev_text == ',' or prev_text[-1] == ',': #if previous text ended with dot or comma
                        if typ != "I": #if current type is not I, aka we are not in the middle of an entity
                            output.write("\n") #we have a new sentence
                
                prev_text = text
                output.write(line) # write the current line
                
            line = fi.readline()
            
    output.close()
    