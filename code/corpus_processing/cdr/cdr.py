# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:37:44 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\cdr.txt"):
    os.remove("1. texts\\cdr.txt")

if os.path.exists("1. annotations\\cdr.txt"):
    os.remove("1. annotations\\cdr.txt")

output1 = open("1. texts\\cdr.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\cdr.txt", "a") #results in order to evaluate NER

num = 0
with open("cdr.txt") as fi:  
   
    line = fi.readline()
    num = 0
    text = ""
    while line:
        line = line.strip('\n')
        line = line.split('\t')
        
        if line[0] != '':#we dont want the empty lines
            if len(line) == 1: 
                line = line[0].split('|t|')#get the title
                if len(line) > 1:
                    text = line[1]
                else: #get the abstract
                    line = line[0].split('|a|')
                    text += " " + line[1] + "\n"
                    output1.write(text)
            elif len(line) > 4:  #the last line of every text is ids
                #get the annotations
                num += 1
                output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, line[4], line[1], line[2], line[3]))
            
        
        line = fi.readline()
        
output1.close()
output2.close()