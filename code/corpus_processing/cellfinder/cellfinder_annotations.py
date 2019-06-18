# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 20:20:31 2019

@author: Αλέξανδρος
"""
import os

if os.path.exists("1. annotations\\cellfinder.txt"):
    os.remove("1. annotations\\cellfinder.txt")

output = open("1. annotations\\cellfinder.txt", "a", encoding="utf8")

dr = os.getcwd() + "\cellfinder" #the folder with the files

num = 0
for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:
        line = fi.readline()
        
        while line:
            line = line.split(None, 4) #dont split the text

            num += 1
            output.write("T{}\t{}\t{}\t{}\t{}".format( num, line[1], line[2], line[3], line[4]))
            
            line = fi.readline()

output.close()