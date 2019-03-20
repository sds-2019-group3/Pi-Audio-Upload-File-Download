#!/usr/bin/env python3
import sys
import subprocess
import requests
import datetime
import time
import logging
import os

logging.basicConfig(filename='/home/pi/AudioRecording/Pi-Audio-Upload-File-Download/logs/file_download.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

host = 'http://sds.samchatfield.com'

#Downloads pdf files and opens them on the pi
def download_files(usr_id, booking_id):
    file_url = host + '/api/user/' + usr_id + '/files'

    #Fetching the json of the files in the current directory
    getReq = requests.get(url = file_url)
    data = getReq.json()
    
    #Creating the directory for temporary files for the current booking
    os.makedirs('temp/' + booking_id, mode = 0o755, exist_ok = True)
    
    #Searching file directory for pdfs and writing them to a temp file
    #to be opened in chrome
    for x in data:
        if ('.pdf' in x['name']):
            logging.info('>>> ' + x['name'] + ' found!')
            file_name = '/' + x['name']

            #Downloading the file and writing it to a temp folder
            getReq = requests.get(host + x['path'])

            with open('temp/' + booking_id + file_name, 'wb') as f:
                f.write(getReq.content)
            
            #Opening the file in chrome
            command = ['chromium-browser', 'temp/' + booking_id + file_name]
            process = subprocess.Popen(command, shell = False)
    return

#Checks when the next booking is and downloads the files for it as well as
#removing the previous booking's files
def check_booking():
    
    #Getting the url to use for the room the pi is assigned to
    current_dt = datetime.datetime.now()
    nxt_booking = current_dt.hour + 1
    book_url = host + '/api/room/CS-225/bookings/' + current_dt.strftime('%Y-%m-%d') + 'T' + str(nxt_booking) + ':00Z'
    
    #Requesting the json data from url for the next booking hour
    getReq = requests.get(url = book_url)
    data = getReq.json()
    
    if (data is None):
        logging.info('>>> No next booking')
        return

    #Converting the string date stored in the json to the default date format
    booking_date = data['start'].replace('T', ' ')
    booking_date = booking_date.replace('Z', '')
    booking_date = datetime.datetime.strptime(booking_date, '%Y-%m-%d %H:%M:%S.%f')

    #Downloads files for the next booking
    current_booking_id = data['_id']
    download_files(data['leader'], current_booking_id)
    
    #Writing the booking id for the next booking, the current and next booking can be
    #stored at the same time
    with open('current_ids.txt', 'a') as id_file:
        id_file.write(current_booking_id + '\n') 
    return

check_booking()
