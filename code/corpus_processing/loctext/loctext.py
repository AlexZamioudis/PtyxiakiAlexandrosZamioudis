# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 01:46:39 2019

@author: Αλέξανδρος
"""

import os
import json

if os.path.exists("1. texts\\loctext.txt"):
    os.remove("1. texts\\loctext.txt")
    
if os.path.exists("1. annotations\\loctext.txt"):
    os.remove("1. annotations\\loctext.txt")

output1 = open("1. texts\\loctext.txt", "a", encoding="utf8")
output2 = open("1. annotations\\loctext.txt", "a", encoding="utf8")

dr = os.getcwd() + "\LocText" #the folder with the files

t = 0
for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    with open(filename) as fi:
        data = json.load(fi)

        text = data.get("text")
        text = text.replace('\n',' ')#remove newline from text
        
        output1.write("{}\n".format(text))
        
        annotations = data.get("denotations")# get annotations
        
        if annotations: #in case it doesnt have any annotations
            start = 0
            end = 0
            for i in annotations:
                span = i.get("span")
                start = span.get("begin")
                end = span.get("end")
                t += 1
                output2.write("T{}\t{}\t{}\t{}\t{}\n".format(t,'genes/proteins', start, end, text[start:end]))
          
output1.close()
output2.close()