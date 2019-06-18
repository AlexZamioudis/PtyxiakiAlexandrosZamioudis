# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 22:27:14 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. annotations\\s800.txt"):
    os.remove("1. annotations\\s800.txt")

output = open("1. annotations\\s800.txt", "a", encoding="utf8")

with open("s800.tsv", encoding="utf8") as fi:  
    
   line = fi.readline()
   num = 0
   while line:
        num += 1
        line = line.split('\t')
        
        output.write("T{}\t{}\t{}\t{}\t{}".format( num, 'species', line[2], line[3], line[4] ))
        
        line = fi.readline()

     
output.close()