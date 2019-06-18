# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:49:16 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. annotations\\linneaus.txt"):
    os.remove("1. annotations\\linneaus.txt")

output = open("1. annotations\\linneaus.txt", "a")

with open("linneaus.tsv") as fi:
    
    line = fi.readline()
    line = fi.readline()#the first line is the types of the columns
    num = 0
    while line:
        num += 1
        line = line.split()
        
        #some entries have a code that we dont want in the text
        #if the last string begins with number it is a code
        if line[-1][0].isalpha():
            text = ' '.join(line[4:])
        else:
            text = ' '.join(line[4:-1])
        
        output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, "species", line[2], line[3], text))
        
        line = fi.readline()
        

output.close()