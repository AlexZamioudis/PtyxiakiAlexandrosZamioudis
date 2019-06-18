# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 22:27:23 2019

@author: Αλέξανδρος
"""

#calais has problems with  non-small files
#seperates a file into one file per line_num lines

import os

dr = os.getcwd() + "\\1. texts" #the folder with the files

for filename in os.listdir(dr):
    name = filename
    name = name.split('.')[0]#remove .txt
    filename = dr + '\\' + filename #the actual path to file
    
    print(name)#just to check progress
    with open(filename, encoding="utf-8") as fi:
        
        line = fi.readline()
        
        num = 0
        file_num = 1 #number of files
        line_num = -1 #sentences number, counts line before a new file is created
        while line:
            
            num += 1
            line_num += 1
            
            if line_num == 5:
                line_num = 0
                file_num += 1
            
            file = "calais_in\\" + name + "\\" + name + str(file_num) + ".txt"
            output = open(file, "a", encoding="utf-8")
            output.write(line)
            output.close()
            
            line = fi.readline()



