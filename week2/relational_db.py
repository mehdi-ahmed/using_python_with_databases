# Schema = The database schema is its structure described in a formal language supported by the database management
# system. The term "schema" refers to the organization of data as a blueprint of how the database is constructed.

# SQL statements examples:


# CREATE TABLE Users(
# 	name VARCHAR(128),
# 	email VARCHAR(128)
# )

# INSERT INTO Users(name, email) VALUES('Kristen', 'krissy@hotmail.com')

# DELETE FROM Users WHERE email='krissy@hotmail.com'

# UPDATE Users SET name = 'Mehdi Ammar' where email='mehdi@myself.com'

# SELECT * from Users

# SELECT * from Users ORDER BY email
# SELECT * from Users ORDER BY name
# SELECT * from Users ORDER BY name DESC

import sqlite3

conn = sqlite3.connect('email_db.sqlite')
curr = conn.cursor()

curr.execute('''
DROP TABLE IF EXISTS Counts''')

curr.execute('CREATE TABLE Counts (email TEXT, count Integer)')

f_name = input('Enter file name: ')
if len(f_name) < 1:
    f_name = 'mbox-short.txt'

fh = open(f_name)
for line in fh:
    if not line.startswith('From: '):
        continue

    pieces = line.split()
    email = pieces[1]
    curr.execute('SELECT count FROM Counts WHERE email = ? ', (email,))  # (email,) tuple
    row = curr.fetchone()

    if row is None:
        curr.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email,))

    else:
        curr.execute('UPDATE Counts SET count = count + 1 WHERE email = ?', (email,))

    conn.commit()

sql_str = 'SELECT email, count FROM Counts ORDER BY count DESC limit 10'
for row in curr.execute(sql_str):
    print(str(row[0]), row[1])

# cwen@iupui.edu 5
# zqian@umich.edu 4
# david.horwitz@uct.ac.za 4
# louis@media.berkeley.edu 3
# gsilver@umich.edu 3
# stephen.marquard@uct.ac.za 2
# rjlowe@iupui.edu 2
# wagnermr@iupui.edu 1
# antranig@caret.cam.ac.uk 1
# gopal.ramasammycook@gmail.com 1


# An sqlite email_db file will be generated
