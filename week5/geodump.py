import codecs
import json
import sqlite3

# DB
conn = sqlite3.connect('geo_data.sqlite')
curr = conn.cursor()

curr.execute('SELECT * FROM Locations')
file_handler = codecs.open('where.js', 'w', 'utf-8')

file_handler.write("myData = [\n")
count = 0

for row in curr:
    data = str(row[1].decode())
    try:
        js = json.loads(str(data))
    except ValueError:
        continue

    if not ('status' in js and js['status'] == 'OK'):
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]

    if lat == 0 or lng == 0:
        continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")
    try:
        print(where, lat, lng)
        count = count + 1
        if count > 1:
            file_handler.write(",\n")

        output = "[" + str(lat) + "," + str(lng) + ", '" + where + "']"
        file_handler.write(output)
    except IOError as e:
        print("error({0}): {1}".format(e.errno, e.strerror))

file_handler.write("\n];\n")
curr.close()
file_handler.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
