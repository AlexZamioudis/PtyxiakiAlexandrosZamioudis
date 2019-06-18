# -*- coding: utf-8 -*-
"""
Created on Mon May  6 02:24:41 2019

@author: Αλέξανδρος
"""
import os

dr = os.getcwd() + "\\1. train iob" #the folder with the files

for filename in os.listdir(dr):
    print(filename) #to check progress
    
    if os.path.exists("1. train iob2\\" + filename):
        os.remove("1. train iob2\\" + filename)
    
    output = open("1. train iob2\\" + filename, "a", encoding="utf8")
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:      
        line = fi.readline()
        
        while line:
            line = line.split('\t')
            
            if len(line) > 1:
                if line[1][0] == 'B' or line[1][0] == 'I':
                    line[1] = line[1].lower()#lower the types for uniformity
                    line[1] = line[1][2:]
                output.write("{}\t{}".format(line[0], line[1]))
            else:
                output.write("\n") #empty line
            
                    
            line = fi.readline()
            
    output.close()      
      