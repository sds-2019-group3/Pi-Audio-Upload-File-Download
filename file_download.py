#!/usr/bin/env python3
import sys
import subprocess
import requests

host = 'http://sds.samchatfield.com'
url = host + '/api/user/1234567/files'

def download_files():
    #Fetching the json of the files in the current directory
    getReq = requests.get(url = url)
    data = getReq.json()
    
    #Searching file directory for pdfs and writing them to a temp file
    #to be opened in chrome
    for x in data:
        if ('.pdf' in x['name']):
            print('>>> ' + x['name'] + ' found!')
            file_name = '/' + x['name']

            #Downloading the file and writing it to a temp folder
            getReq = requests.get(host + x['path'])
            with open('temp' + file_name, 'wb') as f:
                f.write(getReq.content)
            
            #Opening the file in chrome
            command = ['chromium-browser', 'temp' + file_name]
            process = subprocess.Popen(command, shell = False)
    return

download_files()
