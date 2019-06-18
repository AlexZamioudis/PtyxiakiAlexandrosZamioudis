# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 00:30:44 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. annotations 2\\chemdner.txt"):
    os.remove("1. annotations 2\\chemdner.txt")

output = open("1. annotations 2\\chemdner.txt", "a", encoding="utf8")

with open("chemdner_annotations.txt", encoding="utf8") as fi:
    
    line = fi.readline()
    num = 0
    while line:
        num += 1
        line = line.strip('\n')
        line = line.split("\t")
        
        etype = "chemical"
        
        if len(line) != 1:
            output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, etype, line[2], line[3], line[4]))
        
        line = fi.readline()
        

output.close()