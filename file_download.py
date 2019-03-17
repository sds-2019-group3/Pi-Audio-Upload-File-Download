#!/usr/bin/env python3
import sys
import subprocess
import requests
import datetime
import time
import logging

logging.basicConfig(filename='/home/pi/AudioRecording/Pi-Audio-Upload-File-Download/file_download.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

host = 'http://sds.samchatfield.com'

#Downloads pdf files and opens them on the pi
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

#Checks when the next booking is and downloads the files for it as well as
#removing the previous booking's files
def check_booking():
    rm_command = ['rm', 'temp/*']
    
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
    
    #Waiting till the next booking has begun
    logging.info('>>> Waiting for booking')
    start = time.time()
    while(True):
        
        #Checking time to print another waiting message
        end = time.time()
        if ((end - start) >= 180):
            logging.info('>>> Waiting for booking')
            start = time.time()
       
        #Checking if the current time matches the booking
        if (datetime.datetime.now() >= booking_date):
            break
        
    #Removing all files in the temporary storage and downloading those for the next booking
    process = subprocess.Popen(rm_command, shell = False)
    download_files(data['leader'])
    return

check_booking()
