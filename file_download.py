#!/usr/bin/env python3
import sys
import subprocess
import requests
import datetime
from datetime import timedelta

host = 'http://sds.samchatfield.com'

def download_files(usr_id):
    
    file_url = host + '/api/user/' + usr_id + '/files'

    #Fetching the json of the files in the current directory
    getReq = requests.get(url = file_url)
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

def check_booking():
    rm_command = ['rm', 'temp/*']
    current_dt = datetime.datetime.now()
    nxt_booking = current_dt.hour + 1
    book_url = host + '/api/room/CS-225/bookings/' + current_dt.strftime('%Y-%m-%d') + 'T' + str(nxt_booking) + ':00Z'
    getReq = requests.get(url = book_url)
    data = getReq.json()
    
    if (data is None):
        print('>>> No next booking')
        return
        
    while(true):
        if (data.datetime.now() != data['start']):
            break

    process = subprocess.Popen(rm_command, shell = False)
    download_files(data['leader'])

    return

check_booking()
