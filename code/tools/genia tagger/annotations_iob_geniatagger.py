# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:55:02 2019

@author: Αλέξανδρος
"""
import os

dr = os.getcwd() + "\\2. geniatagger results" #the folder with the files

for filename in os.listdir(dr):
    name = filename[:-4]
    
    print(name) #to check progress
    
    name = name + ".iob2"

    if os.path.exists("3. geniatagger iob\\" + name):
        os.remove("3. geniatagger iob\\" + name)
    
    output = open("3. geniatagger iob\\" + name, "a", encoding="utf8")
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:  
        
        line = fi.readline()
        while line:
            line = line.split('\t')
            
            if len(line) > 1:
                output.write("{}\t{}".format(line[0], line[4]))
            else:
                output.write("\n")
            
            line = fi.readline()
            
    output.close()
