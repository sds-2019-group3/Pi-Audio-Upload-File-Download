#!/usr/bin/env python3

import logging
import subprocess
import os
from os import walk
import sys

logging.basicConfig(filename='logs/open_files.log', level=logging.INFO, format='[%(asctime)s] %(message)s')

#Opens pdf files for the current booking in chromium
def open_files(booking_id):
    booking_path = 'temp/' + booking_id
    
    #Checking if the files for the current booking have been downloaded
    if (not(os.path.isdir(booking_path))):
        logging.error('>>> ' + booking_id + ' has not had its files loaded yet!')
        return
    
    #Fetches a list of files for the current booking in the temp directory
    file_list = []
    for (dirpath, dirnames, filenames) in walk(booking_path):
        file_list.extend(filenames)
        break
    
    #Opens all pdfs in chromium which were put into the file list
    for file_name in file_list:
        
        if (not('.pdf' in file_name)):
            continue
        
        #Opening the file in chrome
        command = ['chromium-browser', booking_path + '/' + file_name]
        process = subprocess.Popen(command, shell = False, stderr = subprocess.DEVNULL)
        logging.info('>>> Opened file ' + file_name + ' for booking ' + booking_id)

#Checks if the correct number of parameters have been provided to the script
if (len(sys.argv) != 2):
    logging.error('>>> Booking ID parameter required!')
    sys.exit()    

open_files(sys.argv[1])
