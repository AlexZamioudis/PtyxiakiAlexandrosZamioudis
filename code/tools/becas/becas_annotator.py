# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 00:51:05 2019

@author: Αλέξανδρος
"""

import becas
import os
import xml.etree.ElementTree as ET

if os.path.exists("2. becas results\\jnlpba.xml"):
    os.remove("2. becas results\\jnlpba.xml")

output = open("2. becas results\\jnlpba.xml", "wb")

becas.email = 'example@email.com'

root = ET.Element('root')

num = 0
with open("1. texts\\jnlpba.txt", encoding="utf8") as fi:
    
    line = fi.readline()
    
    while line:
        if line != "\n":
            try:
                num += 1
                results = becas.export_text(line, 'xml')
                
                print(num) #just to check the progress
                root.insert(num, ET.fromstring(results))
            except:
                print("An error occured in line {}".format(num))
        
        line = fi.readline()
        
output.write(ET.tostring(root))
output.close()