#!/usr/bin/env python3
import datetime
import requests
from datetime import timedelta


def post_booking():
    host = 'http://sds.samchatfield.com' 
    book_url = host + '/api/room/CS-225/bookings'
    request = requests.get(book_url)

    current_dt = datetime.datetime.now()
    next_hour_dt = current_dt + timedelta(hours=1)

    time = next_hour_dt.strftime('%Y-%m-%d') + 'T' + next_hour_dt.strftime('%H') + ':00Z'
    print ('>>> ' + time)

    data={"start": time,
            "leader": "1234567",
            "users": ["1234567"]
    }
    
    request = requests.post(book_url, json=data)
    print(request.text)
    return

post_booking()
