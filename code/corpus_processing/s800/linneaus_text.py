# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 21:07:42 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\s800.txt"):
    os.remove("1. texts\\s800.txt")
    
output = open("1. texts\\s800.txt", "a", encoding="utf8")

dr = os.getcwd() + "\s800" #the folder with the files

for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    txt = ""
    with open(filename, encoding="utf8") as fi:
        line = fi.readline()
        while line:
            line = line.replace('\n',' ') #remove the newlines
            txt += line
            line = fi.readline()
            
        txt = ' '.join(txt.split())
        output.write("{}\n".format(txt))
        
output.close()