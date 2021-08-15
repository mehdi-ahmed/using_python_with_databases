# https://www.py4e.com/tools/sql-intro/?PHPSESSID=5edf816bf26c4812d52d4da333cc6e14

import json
import sqlite3

conn = sqlite3.connect('assignment_roster_db.sqlite')
curr = conn.cursor()

# Some setup
curr.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;


CREATE TABLE User (
    id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name       TEXT UNIQUE
);

CREATE TABLE Course (
    id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title      TEXT UNIQUE
);

CREATE TABLE Member (
    user_id         INTEGER,
    course_id       INTEGER,
    role            INTEGER,
    PRIMARY KEY(user_id, course_id)
);
''')

f_name = input('Enter file name: ')
if len(f_name) < 1:
    f_name = 'roster_data.json'

str_data = open(f_name).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    print('Name = ', name, ', Title = ', title, ', Role = ', role)

    curr.execute('INSERT OR IGNORE INTO User (name) values (?)', (name,))
    curr.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = curr.fetchone()[0]

    curr.execute('INSERT OR IGNORE INTO Course (title) values (?)', (title,))
    curr.execute('SELECT id FROM Course WHERE title = ?', (title,))
    course_id = curr.fetchone()[0]

    curr.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) values (?, ?, ?)', (user_id, course_id, role))

    conn.commit()

