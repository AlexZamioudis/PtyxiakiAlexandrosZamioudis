# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 00:01:49 2019

@author: Αλέξανδρος
"""

import os
import xml.etree.ElementTree as ET

if os.path.exists("1. texts\\hprd50.txt"):
    os.remove("1. texts\\hprd50.txt")

if os.path.exists("1. annotations\\hprd50.txt"):
    os.remove("1. annotations\\hprd50.txt")

output1 = open("1. texts\\hprd50.txt", "a") #to be used as input for NER
output2 = open("1. annotations\\hprd50.txt", "a") #results in order to evaluate NER

tree = ET.parse('hprd50.xml')
root = tree.getroot()

for i in root.iter('passage'): #find the texts
    j = i.find('text')
    tmp = j.text
    tmp = ' '.join(tmp.split()) #remove newlines and tabs from the text
    output1.write("{}\n".format(tmp)) 


num = 0
for i in root.iter('annotation'):
    num += 1

    text = i.find('text').text
    start = i.find('location').get('offset')
    end = start + i.find('location').get('length')
    
    output2.write("T{}\t{}\t{}\t{}\t{}\n".format(num, 'protein', start, end, text))

output1.close()
output2.close()