# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 02:27:23 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\osiris.txt"):
    os.remove("1. texts\\osiris.txt")
    
if os.path.exists("1. annotations\\osiris.txt"):
    os.remove("1. annotations\\osiris.txt")

output1 = open("1. texts\\osiris.txt", "a", encoding="utf8")
output2 = open("1. annotations\\osiris.txt", "a", encoding="utf8")
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
            
            output1.write("{}\n".format(text))
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
                            
                        output2.write("T{}\t{}\t{}\t{}\t{}\n".format(t, 'gene', start, end, text[int(start):int(end)]))
                           
                    line = fi.readline()

output1.close()
output2.close()