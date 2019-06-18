# -*- coding: utf-8 -*-
"""
Created on Mon May  6 21:32:23 2019

@author: Αλέξανδρος
"""

import os

dr = os.getcwd() + "\\1. train iob" #the folder with the files

for filename in os.listdir(dr):
    print(filename) #to check progress
    
    if os.path.exists("1. train iob abner\\" + filename):
        os.remove("1. train iob abner\\" + filename)
    
    output = open("1. train iob abner\\" + filename, "a", encoding="utf8")
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:      
        line = fi.readline()
        
        while line:
            line = line.split('\t')
            
            if len(line) > 1:
                line[0] = line[0].replace('|',"") # the '|' char messes up with the training due to being the seperator of words and entities
                line[1] = line[1].replace('|',"")
                text = line[0] + '|' + line[1]
                text = text.strip('\n')
                output.write("{} ".format(text))
            else:
                output.write("\n") #empty line
            
                    
            line = fi.readline()
            
    output.close()
    