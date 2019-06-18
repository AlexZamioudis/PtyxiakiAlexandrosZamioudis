# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:37:39 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. annotations\\deca.txt"):
    os.remove("1. annotations\\deca.txt")

output = open("1. annotations\\deca.txt", "a", encoding="utf8")

with open("deca.txt", encoding="utf8") as fi:
    
    line = fi.readline()
    num = 0
    while line:
        num += 1
        line = line.strip('\n')
        line = line.split("\t")
        
        if len(line) != 1:
            output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, "gene/proteins", line[1], line[2], line[3]))
        
        line = fi.readline()
        

output.close()