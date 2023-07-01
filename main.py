"""
This is the main file of the program. It contains the 
main function that calls the menu function from menu.py
"""

from interface import menu
from masterpwd import verify_masterpwd, create_masterpwd
import sys
from os.path import exists
from os import remove
from database import createdb, encrypt_all
from enckeys import encrypt_file, decrypt_file


hash_file_path = "password_hash.argon2"  # password hash file path
database_path = "password_list.db"      # stored password data base path

# main function


def main():
    try:
        # check if password_hash file that contains hash exists or not
        if exists(hash_file_path):  # if exits then try to match it
            tried_count = 3
            while True:
                tried_count -= 1
                verified = verify_masterpwd(hash_file_path)

                if verified == True:    # if password is verified then break from loop
                    break
                elif tried_count == 0:  # if failed for 3 times exit
                    sys.exit("Too many Tries. Exiting the program...")
                else:
                    print("Wrong Password")

        else:
            create_masterpwd(hash_file_path)

        # if password list database is not detected create a new one
        if not exists(f"{database_path}"):
            print("Creating a new database...")
            createdb(database_path)

        if exists("private.pem.encrypted"):
            try:
                decrypt_file("private.pem")
            except FileNotFoundError:
                pass
        if exists("receiver.pem.encrypted"):
            try:
                decrypt_file("receiver.pem")
            except FileNotFoundError:
                pass

        # calls the menu() from menu.py
        menu()

    except (ValueError, EOFError, KeyboardInterrupt):   # handles all exceptions

        encrypt_all(database_path)
        remove(database_path)   # removes the database file (import os)

        if exists("private.pem"):
            try:
                encrypt_file("private.pem")
            except NameError:
                # if the user quits before entering the master password
                sys.exit("Quitted Prematurely")

        if exists("receiver.pem"):
            try:
                encrypt_file("receiver.pem")
            except NameError:
                # if the user quits before entering the master password
                sys.exit("Quitted Prematurely")

        sys.exit("Quitting the program...")


if __name__ == "__main__":
    main()
