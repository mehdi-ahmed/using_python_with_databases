import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('track_db.sqlite')
curr = conn.cursor()

# Make some fresh tables using executescript()
curr.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id    INTEGER,
    title        TEXT UNIQUE
);

CREATE TABLE Track (
    id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title        TEXT UNIQUE,
    album_id     INTEGER,
    len          INTEGER,
    rating       INTEGER,
    count        INTEGER
);
''')

f_name = input('Enter file name: ')
if len(f_name) < 1:
    f_name = 'Library.xml'


#                <key>Track ID</key>
#                 <integer>369</integer>
#                 <key>Name</key>
#                 <string>Another One Bites The Dust</string>

def lookup(d, key):
    found = False
    for child in d:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(f_name)
all_data = stuff.findall('dict/dict/dict')

print('Dict count:', len(all_data))
for entry in all_data:
    if lookup(entry, 'Track ID') is None:
        continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None:
        continue
    print(name, artist, album, count, rating, length)

    # Artist
    curr.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    # Verification of the last sql statement
    curr.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = curr.fetchone()[0]

    # Album
    curr.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
    # Verification of the last sql statement
    curr.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = curr.fetchone()[0]

    # Track
    curr.execute('''INSERT OR REPLACE INTO Track (title, album_id, len, rating, count)
                VALUES (?, ?, ?, ?, ?)''', (name, album_id, length, rating, count))

    conn.commit()
