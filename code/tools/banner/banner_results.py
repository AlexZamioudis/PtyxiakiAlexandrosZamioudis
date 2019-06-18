# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 01:17:06 2019

@author: Αλέξανδρος
"""

import os

dr = os.getcwd() + "\\2. banner output" #the folder with the files

for filename in os.listdir(dr):
    print(filename) #to check progress
    
    filename1 = filename[:-4] #remove .txt
    filename1 = filename1 + ".iob2"
    
    if os.path.exists("3. banner iob\\" + filename1):
        os.remove("3. banner iob\\" + filename1)
        
    if os.path.exists("3. banner tags\\" + filename):
        os.remove("3. banner tags\\" + filename)
    
    output1 = open("3. banner iob\\" + filename1, "a", encoding="utf-8")
    output2 = open("3. banner tags\\" + filename, "a", encoding="utf-8")

    name = filename
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename, encoding="utf8") as fi:  #open the output file
        
        line = fi.readline()
        while line: #the output file is just an iob file, but with multiple tags in one line
            line = line.strip('\n')
            line = line.split(" ")
            
            for i in line:
                i = i.split('|')
                if len(i) > 1:
                    output1.write("{}\t{}\n".format(i[0], i[1]))
            
            line = fi.readline()
            
    with open("2. banner mention\\" + name, encoding="utf8") as fi:   #open the mention file
        
        num = 0
        line = fi.readline()
        while line: # the mention file is an modified version of bc2 annotation files
            line = line.strip('\n')
            line = line.split("|")
            
            if len(line) > 1 :
                etype = line[1]
                ent = line[3]
                
                tmp = line[2].split(" ")
                start = tmp[0]
                end = tmp[1]
                
                num += 1
                output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, etype, start, end, ent))
            
            line = fi.readline()
    
    output1.close()
    output2.close()