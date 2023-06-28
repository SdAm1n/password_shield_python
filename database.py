import sqlite3
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


def storepwd():
    ...


def findpwd():
    ...


def changepwd():
    ...


def deletepwd():
    ...


def deletedb():
    ...


def printall(db_path):
    conn, cur = connectdb(db_path)

    cur.execute("SELECT * FROM plist")

    records = cur.fetchall()
    headers = [i[0] for i in cur.description]

    records = [record[1:] for record in records]
    headers = headers[1:]
    # You must decrypt the password before printing
    print(tabulate(records, headers=headers, tablefmt="fancy_grid"))

    closedb(conn)
