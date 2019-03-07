#!/usr/bin/env python3
import sys
import subprocess
import requests

host = 'http://sds.samchatfield.com'
url = 'http://sds.samchatfield.com/api/user/1234567/files'
#!/usr/bin/env python3

def download_files():
    request = requests.get(url = url)
    data = request.json()
    
    for x in data:
        if ('.pdf' in x['name']):
            print('pdf found!')
            file_name = '/' + x['name']
            print('The download url ' + host + x['path'])
            request = requests.get(host + x['path'])
            with open('temp' + file_name, 'wb') as f:
                f.write(request.content) 
        else:
            print('Not a pdf!')
    return

download_files()
