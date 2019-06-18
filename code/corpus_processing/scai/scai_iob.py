# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:43:46 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. iob\\scai_disease.iob2"):
    os.remove("1. iob\\scai_disease.iob2")
    
output = open("1. iob\\scai_disease.iob2", "a", encoding="utf8")


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
                tmp = line[3].split("-") #is it I or O
                if len(tmp) > 1:
                    output.write("{}\tI-Disease\n".format(text))
                else:
                    output.write("{}\tO\n".format(text))
            else: 
                line[4] = line[4].strip('\n')
                output.write("{}\tB-Disease\n".format(text))
        
        line = fi.readline()

output.close()