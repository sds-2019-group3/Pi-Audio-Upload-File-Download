#!/usr/bin/env python3

import socket
import subprocess
import time
import logging

logging.basicConfig(filename='logs/NFC_comm.log', level=logging.DEBUG, format='[%(asctime)s] %(message)s')

ip = "localhost"
port = 1337

# Shell command for port forwarding. This allows us to communicate over ADB
command = "sudo adb forward tcp:1337 tcp:1337"
process = subprocess.Popen(command.split())

# Make socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server on other end
s.connect((ip, port))
logging.info("Connected on " + ip + ":" + str(port))

# Loop
while True:
    try:
        # Get the length of the room name so we know how many bytes to expect
        string_length = int(s.recv(4))
        booking_id = s.recv(string_length)
        
        if booking_id:    
            subprocess.Popen(['python3', 'open_files.py', booking_id], shell = False) 
    except ValueError: 
        # In this case, we have received some null data. Only bad things can cause this 
        #such as unplugging the USB cable, or quitting the server phone-side
        logging.error('Something went wrong, maybe the connection broke? Shutting down.')
        break
    except KeyboardInterrupt:
        logging.error('>>> Received keyboard interrupt. Shutting down.')
        break
