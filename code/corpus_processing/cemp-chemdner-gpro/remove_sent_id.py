# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:06:45 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. test no id\\scai_disease.txt"):
    os.remove("1. test no id\\scai_disease.txt")

output = open("1. test no id\\scai_disease.txt", "a", encoding="utf8")

with open("1. train test 2\\scai_disease_test.txt", encoding="utf8") as fi:  
    
   line = fi.readline()
   
   while line:
       newline = line.split(None, 1)[1]#just remove the first word
       output.write(newline)
       
       line = fi.readline()
      
output.close()