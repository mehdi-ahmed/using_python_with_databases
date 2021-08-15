# https://www.py4e.com/tools/sql-intro/?PHPSESSID=1266841610f4725f587afea15efd328c

import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('itunes_db.sqlite')
curr = conn.cursor()

# Make some fresh tables using executescript()
curr.executescript('''

DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

''')


def lookup(d, key):
    found = False
    for child in d:
        if found:
            return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


f_name = input('Enter file name: ')
if len(f_name) < 1:
    f_name = 'Library.xml'

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
    genre = lookup(entry, 'Genre')

    if name is None or artist is None or album is None or genre is None:
        continue

    print('Name = ', name, '', ', Artist = ', artist, ', Album = ', album, ', Genre = ', genre, ', Count = ', count,
          ', Rating = ', rating, ', Length = ', length)

    # Artist
    curr.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    # Verification of the last sql statement
    curr.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = curr.fetchone()[0]

    # Genre
    curr.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    curr.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = curr.fetchone()[0]

    # Album
    curr.execute('INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)', (album, artist_id))
    # Verification of the last sql statement
    curr.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = curr.fetchone()[0]

    # Track
    curr.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count)
                    VALUES (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, length, rating, count))

    conn.commit()
