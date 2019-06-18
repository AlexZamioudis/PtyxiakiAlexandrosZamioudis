# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:32:05 2019

@author: Αλέξανδρος
"""

import os
import random

seed = 2019 #the seed with wich we randomize the list
tt_split = 0.30 #how much of the text we use for the testing

dr = os.getcwd() + "\\1. bc2 texts" #the folder with the texts
dr2 = os.getcwd() + "\\1. bc2 annotations 2" #the folder with the annotations

for filename in os.listdir(dr):
    name = filename[:-4]
    
    print(name) #to check progress

    #the annotation files to be generated
    if os.path.exists("1. train test 2\\" + name + "_train.txt"):
        os.remove("1. train test 2\\" + name + "_train.txt")
    
    if os.path.exists("1. train test 2\\" + name + "_test.txt"):
        os.remove("1. train test 2\\" + name + "_test.txt")
    
    output1 = open("1. train test 2\\" + name + "_train.txt", "a", encoding="ascii")
    output2 = open("1. train test 2\\" + name + "_test.txt", "a", encoding="ascii")
    
    #the annotation files to be generated
    if os.path.exists("1. train test 2\\" + name + "_train.ann"):
        os.remove("1. train test 2\\" + name + "_train.ann")
    
    if os.path.exists("1. train test 2\\" + name + "_test.ann"):
        os.remove("1. train test 2\\" + name + "_test.ann")
    
    output3 = open("1. train test 2\\" + name + "_train.ann", "a", encoding="ascii")
    output4 = open("1. train test 2\\" + name + "_test.ann", "a", encoding="ascii")
    
    filename = dr + '\\' + filename #the actual path to the text file
    filename2 = dr2 + '\\' + name + '.ann' #the actual path to the annotation file
    
    text = []
    with open(filename, encoding="utf8") as fi:  
        line = fi.readline()
        
        while line:
            if len(line.strip('\n')) > 0:
                text.append(line)
            
            line = fi.readline()
    
    annotations = []
    with open(filename2, encoding="utf8") as fi:  
        line = fi.readline()
        
        while line:
            if len(line.strip('\n')) > 0:
                annotations.append(line)
            
            line = fi.readline()
            
    random.seed(seed)
    random.shuffle(text)
    random.shuffle(annotations)
    
    #write text
    point = int(len(text) * tt_split)
    test_text = text[:point]
    train_text = text[point:]

    for i in train_text:
        output1.write(i)

    for i in test_text:
        output2.write(i)
    
    #write annotations
    point = int(len(annotations) * tt_split)
    test_text = annotations[:point]
    train_text = annotations[point:]

    for i in train_text:
        output3.write(i)

    for i in test_text:
        output4.write(i)
        
    output1.close()
    output2.close()
    output3.close()
    output4.close()
    