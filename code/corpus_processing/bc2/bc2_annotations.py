# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 22:07:58 2019

@author: Αλέξανδρος
"""
import os

if os.path.exists("1. annotations\\bc2.txt"):
    os.remove("1. annotations\\bc2.txt")

output = open("1. annotations\\bc2.txt", "a")

with open("GENE.eval") as fi:
    
    line = fi.readline()
    num = 0
    while line:
        num += 1
        line = line.split("|")
        
        """
        split the start and end positions since they are seperated by space
        while we need them to be seperated by tab 
        """
        line[1] = line[1].split() 
        output.write("T{}\t{}\t{}\t{}\t{}".format(num, "genes/proteins", line[1][0], line[1][1], line[2]))
        
        line = fi.readline()
        

output.close()