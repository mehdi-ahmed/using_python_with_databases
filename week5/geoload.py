# Google Places API set up https://developers.google.com/maps/documentation/places/web-service/cloud-setup
# Examples
# https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=500&types=food&name=harbour
# &key=AIzaSyBwaGnuc4Sbs1ifLbsmpncGjfYxWR1SgX0
import json
import sqlite3
import ssl
import time
import urllib.parse
import urllib.request

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

api_key_usage = True
# If you have a Google Places API Key, enter it here
api_key = 'AIzaSyBwaGnuc4Sbs1ifLbsmpncGjfYxWR1SgX0'

if api_key is False:
    service_url = 'http://py4e-data.dr-chuck.net/geojson?'
else:
    service_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'

# Additional details for urllib
# http.client.HTTPConnection.debuglevel = 1

# DB
conn = sqlite3.connect('geo_data.sqlite')
curr = conn.cursor()
curr.executescript('''
   CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)
''')

# Data File
fh = open('where.data')
count = 1
for line in fh:
    if count >= 300:
        print('Retrieved 300 locations, restart to retrieve more')
        break
    address = line.strip()
    print(line.strip(), ', Count = ', count)

    # Return a copy of the string with leading and trailing whitespace removed.
    # If chars is given and not None, remove characters in chars instead.
    print('')
    curr.execute('SELECT geodata FROM Locations WHERE address = ?', (memoryview(address.encode()),))

    # If it is already in DB, continue
    try:
        data = curr.fetchone()
        if data is None:
            print('Select did not find any geodata')
        else:
            print('Found in DB', address)
            continue

    except sqlite3.Error:
        pass

    params = dict()
    params["query"] = address
    if api_key is not False:
        params['key'] = api_key

    url = service_url + urllib.parse.urlencode(params)

    print('Retrieving URL...', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieving', len(data), 'characters')
    count = count + 1

    try:
        js = json.loads(data)
    except ValueError as e:
        print(data)  # We print in case Unicode causes an error
        print("error at", json.JSONDecodeError.msg)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('======Failure to retrieve========')
        print(data)
        break

    curr.execute(''' INSERT OR IGNORE INTO Locations (address, geodata) VALUES (?, ?)''',
                 (memoryview(address.encode()), memoryview(data.encode())))

    conn.commit()
    if count % 10 == 0:
        print('Pausing for a bit')
        time.sleep(5)

    print('Run geodump.py to read  the data from the DB so you can visualize it on a map.')
