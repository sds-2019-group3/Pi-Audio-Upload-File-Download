#!/usr/bin/env python3
import subprocess
import sys
import requests

recording_name = "recording.wav"

def record_audio(s_hours):
    #Converting hours to seconds
    duration = float(s_hours) * (60**2)

    #Command used to record audio, duration is the amount of time to record in seconds
    record_comm = ["arecord", "-D", "sysdefault:CARD=VX5000", "-d", str(int(duration)), "-f", "cd", recording_name]
    process = subprocess.Popen(record_comm, shell=False, stderr=subprocess.PIPE)
    
    #Checking for any output from the command and printing it to the terminal
    while True:
        error_output = process.stderr.read(1)
        if (process.poll() != None):
            break
        if (error_output != ''):
            sys.stdout.write(error_output.decode("utf-8"))
            sys.stdout.flush()
    return

def post_recording(s_record_name):
    url = "http://sds.samchatfield.com/api/user/1234567/files"
    request = requests.get(url)

    if (request.status_code != 200):
        print("Upload failed, status code ", request.status_code)
        return

    files = {'file': open(s_record_name, 'rb')}
    request = requests.post(url, files=files)
    print(">>> Uploaded files!")
    return

if (len(sys.argv) != 2):
    print("Duration of audio recording is required!")
    sys.exit()

record_audio(sys.argv[1])
print (">>> Audio recording done!")
print(">>> Uploading file now")
post_recording(recording_name)


