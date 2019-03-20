#!/usr/bin/env python3
import logging
import subprocess
import os

logging.basicConfig(filename='/home/pi/AudioRecording/Pi-Audio-Upload-File-Download/logs/remove_files.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

latest_id = ''
text_file = "current_ids.txt"

#Removes all files in the temp directory which are not for the latest
#booking
def remove_file_ids():
    global latest_id
    global text_file

    remove_command = 'rm -r '
    
    #Opens the text file which stores the booking ids which are currently in running
    #and stores the most recent booking added
    with open(text_file, 'r') as id_file:
        lines = id_file.read().splitlines()
    
    #Checking if any booking files are currently being stored
    if (len(lines) == 0):
        logging.info('>>> No ongoing bookings')
        return

    latest_id = lines[-1]

    if (latest_id == ''):
        logging.info('>>> No ongoing bookings')
        return

    #Lists all folders in the temp directory where booking files are stored
    file_id_lst = next(os.walk('./temp'))[1]

    #Looping over each of the ids in the temp folder and deleting the folder
    #if the name of the folder does not match the booking id which was most recently added
    for file_id in file_id_lst:
        if (file_id == latest_id):
            continue
        else:
            current_command = remove_command + 'temp/' + file_id
            process = subprocess.Popen(current_command, shell = True)
            logging.info('>>> Removed file with booking ID: ' + file_id)
    return

#Removes the old booking ids from the text file and keeps the latest id in the
#text file
def remove_txt_ids():
    global latest_id
    global text_file

    if (latest_id == ''):
        return
    
    #Reducing the size of the file to 0 and then writing the latest id to it
    with open(text_file, 'w+') as id_file:
        id_file.truncate(0)
        id_file.write(latest_id + '\n')
    return

remove_file_ids()
remove_txt_ids()
