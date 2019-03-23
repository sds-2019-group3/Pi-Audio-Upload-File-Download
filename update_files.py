#!/usr/bin/env python3
import socketio
import requests
import datetime
import logging
import sys
import time

logging.basicConfig(filename='logs/update_files.log', level=logging.INFO, format='[%(asctime)s] %(message)s')
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
host = 'http://sds.samchatfield.com'

#Downloads files which are uploaded to the server for the current booking
def download_files(booking_id, end_time):
    #Converting the given end time to a time type rather than
    #a string
    temp_end_time = end_time.replace('T', ' ')
    temp_end_time = temp_end_time.replace('Z', '')
    conv_end_time = datetime.datetime.strptime(temp_end_time, '%Y-%m-%d %H:%M:%S.%f')
    sio = socketio.Client(logger=False)
    
    #Tells the server what the booking id for the session is when the client
    #connects, also logs the connection
    @sio.on('connect')
    def on_connect():
        sio.emit('bookingId', booking_id)
        logging.info('>>> Connected to server for booking id: ' + booking_id)

    #Adds new files uploaded for the booking
    @sio.on('new files')
    def on_new_files(data):
        
        #For each file added we download it to the correct path and log it
        for data_dict in data:
            request = requests.get(host + data_dict['path'])
            file_name = '/' + data_dict['name']
            with open('temp/' + booking_id + file_name, 'wb') as f:
                f.write(request.content)
            logging.info('>>> File: ' + data_dict['name'] + ' added to booking: ' + booking_id)
   
    #Connecting to the server
    sio.connect('http://sds.samchatfield.com', socketio_path = '/api/booking/file-socket')
    
    #Continuously loops until the booking is over
    while(True):
        current_time = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        logging.info('>>> Waiting for end, current time: ' + current_time + ', end time: ' + end_time)

        if (datetime.datetime.now() >= conv_end_time):
            sio.emit('disconnect')
            sio.disconnect()
            logging.info('>>> Terminated connection with server for booking id: ' + booking_id)
            return

        time.sleep(120)

#Checking if the correct number of arguments has been passed
if (len(sys.argv) != 3):
    logging.error('>>> Parameters booking ID and end time of booking are required!')
    sys.exit()    

download_files(sys.argv[1], sys.argv[2])
