# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 00:39:03 2019

@author: Αλέξανδρος
"""
import os
from nltk.tokenize import sent_tokenize

# GeniaTagger wants its input files to be one sentence per line
# A lot of files are already in this form and thats why this process is done by selecting each file seperatly

if os.path.exists("geniatagger_scai_disease.txt"):
    os.remove("geniatagger_scai_disease.txt")

output = open("geniatagger_scai_disease.txt", "a", encoding="utf8")

with open("1. texts\\scai_disease.txt", encoding="utf8") as fi:  
    
    line = fi.readline()
   
    while line:
        line = sent_tokenize(line)
        
        for i in line:
            output.write("{}\n".format(i))
          
        line = fi.readline()
      
output.close()