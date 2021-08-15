# https://www.py4e.com/tools/sql-intro/?PHPSESSID=a7e41b5fd19edc948add6b96bb6f28f4


# This application will read the mailbox data (mbox.txt) and count the number of email messages per organization
# (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

# CREATE TABLE Counts (org TEXT, count INTEGER)


# When you have run the program on mbox.txt upload the resulting database file above for grading.

# If you run the program multiple times in testing or with different files, make sure to empty out the data before
# each run.

# Because the sample code is using an UPDATE statement and committing the results to the database as each record is
# read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely
# writing all the data to disk every time it is called.

# The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program,
# there is a balance between the number of operations you execute between commits and the importance of not losing
# the results of operations that have not yet been committed.

import re
import sqlite3

conn = sqlite3.connect('assignment_email_db.sqlite')
curr = conn.cursor()

curr.execute('DROP TABLE IF EXISTS Counts')
curr.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')


# Using regex to retrieve domain name of the email address(organisation)
def get_organisation(org):
    return re.findall('.*@([^ ]*)', org)


f_name = input('Enter file name: ')
if len(f_name) < 1:
    f_name = 'mbox.txt'

fh = open(f_name)

emails = list()
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    emails.append(pieces[1])

emails_dict = dict()
for email in emails:
    organisation = get_organisation(email)[0]
    emails_dict[organisation] = emails_dict.get(organisation, 0) + 1

# print(counts)
for domain in emails_dict:
    # print(domain, '->', emails_dict[domain])

    curr.execute('SELECT org FROM Counts WHERE org = ? ', (domain,))
    row = curr.fetchone()
    if row is None:
        curr.execute('INSERT INTO Counts (org, count) VALUES (?, ?)''', (domain, emails_dict[domain]))
    else:
        curr.execute('UPDATE Counts SET count = ? WHERE org = ?', (emails_dict[domain], domain))

conn.commit()

# https://www.sqlite.org/lang_select.html
sql_str = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 100'

print('--------------------')
for row in curr.execute(sql_str):
    print(str(row[0]), row[1])

curr.close()
