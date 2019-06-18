# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 00:41:39 2019

@author: Αλέξανδρος
"""
import os


if os.path.exists("3. calais tags\\arizona.txt"):
    os.remove("3. calais tags\\arizona.txt")
    
output = open("3. calais tags\\arizona.txt", "a", encoding="utf8")

dr = os.getcwd() + "\calais_out\\arizona" #the folder with the files
num = 0
for filename in os.listdir(dr):
    
    filename = dr + '\\' + filename #the actual path to file
    
    e_type = "" #entity type
    #some times the same entity is found multiple times,
    #so we get the previous entity type

    with open(filename, encoding="utf-8") as fi:
        
        line = fi.readline()
        
        
        while line:
            line = line.split('exact":"') #find the entities in "exact":"entity"
            
            for i in range(1,len(line)):
                entity = line [i] [ 0 : line[i].find('"') ] #get the entity
                
                #get the start of the entity, its in "offset":start,"length"
                start = line [i] [ ( line[i].find('"offset":') + 9) : line[i].find(',"length"') ] 
                
                end = int(start) + len(entity) #the end of the entity
                
                ent = line[i-1] #find the entity type in "_type":"entity type"
                ent = ent.split('_type":"')
                
                if len(ent) > 1:#get the entity
                    e_type = ent[1][ 0 : ent[1].find('"') ]
                
                num += 1
                output.write("T{}\t{}\t{}\t{}\t{}\n".format(num, e_type, start, end, entity))
            
            line = fi.readline()
            
            
output.close()