# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:15:01 2019

@author: Αλέξανδρος
"""

import sys
import requests
import os
calais_url = 'https://api.thomsonreuters.com/permid/calais'
def main(a,b,c):
    try:
        if not a or not b or not c:
            print ('3 params are required: 1.input file full path, 2.output directory and 3.access token')
            sys.exit(-1)
        else:
            input_file = a
            output_dir = b
            access_token = c
            
            if not os.path.exists(input_file):
                print ('The file [%s] does not exist' % input_file)
                return
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
        headers = {'X-AG-Access-Token' : access_token, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
        #headers = {'X-AG-Access-Token' : access_token, 'Content-Type' : 'application/pdf', 'outputformat' : 'application/json'}
        sendFiles(input_file, headers, output_dir)
    except Exception as e:
        print ('Error in connect ', e)

def sendFiles(files, headers, output_dir):
    is_file = os.path.isfile(files)
    if is_file == True:
        sendFile(files, headers, output_dir)
    else:
        for file_name in os.listdir(files):
            file_name = files + "\\" + file_name
            if os.path.isfile(file_name):
                sendFile(file_name, headers, output_dir)
            else:
                sendFiles(file_name, headers, output_dir)

def sendFile(file_name, headers, output_dir):
    with open(file_name, 'rb') as input_data:
        response = requests.post(calais_url, data=input_data, headers=headers, timeout=80)
        print ('status code: %s' % response.status_code)
        content = response.text
        print ('Results received: %s' % content)
        if response.status_code == 200:
            saveFile(file_name, output_dir, content)

def saveFile(file_name, output_dir, content):
    output_file_name = os.path.basename(file_name) + '.xml'
    output_file = open(os.path.join(output_dir, output_file_name), 'wb')
    output_file.write(content.encode('utf-8'))
    output_file.close()

if __name__ == "__main__":
   main()