import sqlite3
# tabulate is used to print the table in a nice format
from tabulate import tabulate


# Connect to a database
def connectdb(db_path):
    # connect to database
    conn = sqlite3.connect(db_path)

    # create a cursor
    cur = conn.cursor()

    return conn, cur


# close the connection from a database
def closedb(conn):
    # commit the changes to database
    conn.commit()

    # close connection
    conn.close()


# create database and table
def createdb(db_path):

    conn, cur = connectdb(db_path)

    # execute create table command
    cur.execute("""CREATE TABLE plist (
        id INTEGER PRIMARY KEY,
        website TEXT,
        username TEXT,
        password TEXT
    )
    """)

    closedb(conn)


# adjust the id field if deleted
def adjustid(db_path):
    conn, cur = connectdb(db_path)

    cur.execute("SELECT id FROM plist ORDER BY id")
    ids = cur.fetchall()

    new_id = 1
    for id in ids:
        cur.execute("UPDATE plist SET id=? WHERE id=?", (new_id, id[0]))
        new_id += 1

    closedb(conn)


# print the table in a nice format
def prettyprint(records, headers):
    print(tabulate(records, headers=headers, tablefmt="fancy_grid"))


# store password in database
def storepwd(db_path, website, username, password):

    conn, cur = connectdb(db_path)

    cur.execute("""INSERT INTO plist (website, username, password)
        VALUES (?, ?, ?)
    """, (website, username, password))

    closedb(conn)


def findpwd(db_path, findby):
    conn, cur = connectdb(db_path)
    # TODO: Decrypt the password before printing
    if findby == 'w':
        website = input("Enter website: ")
        cur.execute("SELECT * FROM plist WHERE website=?", (website,))
    elif findby == 'u':
        username = input("Enter username: ")
        cur.execute("SELECT * FROM plist WHERE username=?", (username,))

    records = cur.fetchall()
    headers = [i[0] for i in cur.description]
    prettyprint(records, headers)

    closedb(conn)


def changepwd():
    ...


def deletepwd():
    ...


def deletedb():
    ...


# prints all the records from the database except id
def printall(db_path):
    conn, cur = connectdb(db_path)

    cur.execute("SELECT * FROM plist")

    records = cur.fetchall()
    headers = [i[0] for i in cur.description]

    # records = [record[1:] for record in records]
    # headers = headers[1:]
    # TODO: Decrypt the password before printing
    prettyprint(records, headers)
    closedb(conn)
