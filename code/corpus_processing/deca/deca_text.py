# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:58:55 2019

@author: Αλέξανδρος
"""

import os

if os.path.exists("1. texts\\deca.txt"):
    os.remove("1. texts\\deca.txt")
    
output = open("1. texts\\deca.txt", "a", encoding="utf8")

dr = os.getcwd() + "\DECA" #the folder with the files

for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    txt = ""
    with open(filename, encoding="utf8") as fi:
        line = fi.readline()
        while line:
            line = line.replace('\n',' ')
            txt += line
            line = fi.readline()
            
        txt = ' '.join(txt.split())
        output.write("{}\n".format(txt))
        
output.close()