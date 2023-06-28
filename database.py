import sqlite3
# tabulate is used to print the table in a nice format
from tabulate import tabulate
from hybridenc import *

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
        website TEXT,
        username TEXT,
        enc_session_key BLOB,
        nonce BLOB,
        tag BLOB,
        ciphertext BLOB
    )
    """)

    closedb(conn)


# print the table in a nice format
def prettyprint(records, headers):

    new_records = []
    for row in range(len(records)):

        password = decryptpwd(records[row][2],
                              records[row][3], records[row][4], records[row][5])
        new_records.append(
            (records[row][0], records[row][1],  password))

    headers = headers[0], headers[1], "password"
    print(tabulate(new_records, headers=headers, tablefmt="fancy_grid"))


# store password in database
def storepwd(db_path, website, username, password):

    conn, cur = connectdb(db_path)

    # TODO: Encrypt the password before storing
    password = password.encode("utf-8")
    enc_session_key, nonce, tag, ciphertext = encryptpwd(password)
    cur.execute("""INSERT INTO plist (
        website, username, enc_session_key, nonce, tag, ciphertext)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
                (website, username, memoryview(enc_session_key), memoryview(nonce), memoryview(tag), memoryview(ciphertext)))

    closedb(conn)


# find password in database
def findpwd(db_path, findby):

    conn, cur = connectdb(db_path)
    if findby == 'w':
        website = input("Enter website: ")
        cur.execute("SELECT * FROM plist WHERE website=?", (website,))
    elif findby == 'u':
        username = input("Enter username: ")
        cur.execute("SELECT * FROM plist WHERE username=?", (username,))

    # TODO: Decrypt the password before printing
    records = cur.fetchall()

    headers = [i[0] for i in cur.description]
    prettyprint(records, headers)

    closedb(conn)


# change password in database
def changepwd(db_path):

    printall(db_path)

    conn, cur = connectdb(db_path)

    print("Enter the website, username and new password to change the password")

    website = input("Enter website: ")
    username = input("Enter username: ")
    password = input("Enter new password: ")

    # Encrypt the password before storing
    password = password.encode("utf-8")
    enc_session_key, nonce, tag, ciphertext = encryptpwd(password)
    cur.execute("""UPDATE plist SET enc_session_key=?, nonce=?, tag=?, ciphertext=? 
                WHERE website=? AND username=?""",
                (memoryview(enc_session_key), memoryview(nonce), memoryview(tag), memoryview(ciphertext), website, username))

    closedb(conn)


# delete password in database
def deletepwd(db_path):

    printall(db_path)

    conn, cur = connectdb(db_path)

    print("Enter the website and username to delete the password")

    website = input("Enter website: ")
    username = input("Enter username: ")
    cur.execute("""DELETE FROM plist 
                    WHERE website=? AND username=?""",
                (website, username))

    closedb(conn)


# delete the database
def deletedb(db_path):

    conn, cur = connectdb(db_path)

    cur.execute("DROP TABLE plist")

    closedb(conn)


# prints all the records from the database except id
def printall(db_path):
    conn, cur = connectdb(db_path)
    # conn.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM plist")

    records = cur.fetchall()

    headers = [i[0] for i in cur.description]

    # records = [record[1:] for record in records]

    # Decrypt the password before printing
    prettyprint(records, headers)
    closedb(conn)
