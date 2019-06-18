# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 00:45:52 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. iob1\\scai_disease.iob2"):
    os.remove("1. iob1\\scai_disease.iob2")
    
output = open("1. iob1\\scai_disease.iob2", "a", encoding="utf8")


with open("SCAI disease.txt", encoding="utf8") as fi:      
   line = fi.readline()
   num = 0
   while line:
        line = line.replace('\t\t','\t')#remove double tabs
        line = line.split('\t')
        
        if len(line) == 1:
            line = fi.readline()
            output.write("\n")
            continue #for the empty lines or ids in the text
        else:
            text = line[0]
            
            if len(line) == 4:#in the begining of the entity, the full name is given
                line[3] = line[3].strip('\n')
                output.write("{}\t{}\n".format(text, line[3][1:]))#dont get the |
            else: 
                line[4] = line[4].strip('\n')
                output.write("{}\t{}\n".format(text, line[4][1:]))#dont get the |
        
        line = fi.readline()

output.close()