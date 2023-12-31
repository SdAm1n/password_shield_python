"""
This file contains functions for creating, retrieving, 
updating and deleting passwords from the database.
This file also contains functions for printing the table in a nice format.
This file also contains functions for encrypting and decrypting passwords.
This file also encrypts and decrypts the database.
"""

from time import time
from pysqlcipher3 import dbapi2 as sqlite
import sqlite3
# tabulate is used to print the table in a nice format
from tabulate import tabulate
from hybridenc import *
from masterpwd import get_masterpwd
from rsaenc import rsa_encrypt, rsa_decrypt, rsa_keygen


def enc_connectdb(db_path):
    # connect to database
    conn = sqlite.connect(db_path)

    # create a cursor
    cur = conn.cursor()

    # set key for database from user password
    cur.execute(f"PRAGMA key='{get_masterpwd()}'")
    # for SQLCipher compatibility
    cur.execute("PRAGMA cipher_compatibility = 3")

    return conn, cur


# Connect to a database
def connectdb(db_path):

    # connect to database
    conn = sqlite3.connect(db_path)

    # create a cursor
    cur = conn.cursor()

    # set key for database from user password
    # cur.execute(f"PRAGMA key='{get_masterpwd()}'")
    # # for SQLCipher compatibility
    # cur.execute("PRAGMA cipher_compatibility = 3")

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
    start = time()
    conn, cur = connectdb(db_path)
    # conn.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM plist")

    records = cur.fetchall()

    headers = [i[0] for i in cur.description]

    # records = [record[1:] for record in records]

    # Decrypt the password before printing
    prettyprint(records, headers)
    closedb(conn)
    end = time()
    print(end - start)


def encrypt_all(db_path):

    print("generating rsa keys...")
    rsa_keygen()
    print("rsa keys generated...")

    print("encrypting database...")

    new_db_path = f"enc_{db_path}"

    conn, cur = enc_connectdb(new_db_path)

    # execute create table command to store encrypted passwords in newly created database
    cur.execute("""CREATE TABLE encplist (
        website BLOB,
        username BLOB,
        enc_session_key BLOB,
        nonce BLOB,
        tag BLOB,
        ciphertext BLOB
    )
    """)
    conn.commit()

    conn2, cur2 = connectdb(db_path)
    cur2.execute("SELECT * FROM plist")
    conn2.commit()
    records = cur2.fetchall()
    # print(records[0][0])
    for row in range(len(records)):
        website = rsa_encrypt(records[row][0].encode("utf-8"))
        username = rsa_encrypt(records[row][1].encode("utf-8"))
        enc_session_key = records[row][2]
        nonce = rsa_encrypt(records[row][3])
        tag = rsa_encrypt(records[row][4])
        ciphertext = rsa_encrypt(records[row][5])

        cur.execute("""INSERT INTO encplist (
            website, username, enc_session_key, nonce, tag, ciphertext)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
                    (memoryview(website), memoryview(username), memoryview(enc_session_key), memoryview(nonce), memoryview(tag), memoryview(ciphertext)))
        conn.commit()

    print("deleting old database...")

    closedb(conn2)
    closedb(conn)

    print("database encrypted...")


def decrypt_all(db_path):

    print("decrypting database...")

    conn, cur = connectdb(db_path)

    conn2, cur2 = enc_connectdb(f"enc_{db_path}")

    cur2.execute("SELECT * FROM encplist")
    records = cur2.fetchall()
    for row in range(len(records)):
        website = rsa_decrypt(records[row][0]).decode("utf-8")
        username = rsa_decrypt(records[row][1]).decode("utf-8")
        enc_session_key = records[row][2]
        nonce = rsa_decrypt(records[row][3])
        tag = rsa_decrypt(records[row][4])
        ciphertext = rsa_decrypt(records[row][5])

        cur.execute("""INSERT INTO plist (
            website, username, enc_session_key, nonce, tag, ciphertext)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
                    (website, username, memoryview(enc_session_key), memoryview(nonce), memoryview(tag), memoryview(ciphertext)))
        conn.commit()
    closedb(conn2)
    closedb(conn)
    print("database decrypted...")
