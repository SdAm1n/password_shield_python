"""
This file contains the menu function which is used to display the menu to the user
and call the functions from other files according to the user's choice.
"""

from genpwd import generatepwd
import os
import sys
import database
from enckeys import encrypt_file, decrypt_file
import pyperclip


database_path = "password_list.db"


# to clear terminal
def cliearscr():
    if os.name == "nt":     # for detecting windows operating system
        os.system("cls")
    else:                   # for detecting linux/mac (os.name == "posix")
        os.system("clear")


# a simple menu function
def menu():
    # calling until user quits
    cliearscr()
    if os.path.exists(f"enc_{database_path}"):
        database.decrypt_all(database_path)
        os.remove(f"enc_{database_path}")

    while True:

        print("\nMENU")
        print("-----------------")
        print("(G)enearate Password")
        print("(S)tore Password")
        print("(F)ind Password")
        print("(C)hange Password")
        print("(D)elete")
        print("(A)ll Password")
        print("(Q)uit")
        try:
            option = input("Enter Choice: ").lower()
        except ValueError:  # if user inputs invalid Choice
            print("Enter a valid Choice: ")
        else:

            if option == 'q':

                database.encrypt_all(database_path)
                os.remove(database_path)

                if os.path.exists("private.pem"):
                    encrypt_file("private.pem")

                if os.path.exists("receiver.pem"):
                    encrypt_file("receiver.pem")

                sys.exit("Quiting the program....")

            elif option == 'g':
                cliearscr()
                generated_pwd = generatepwd()
                pyperclip.copy(generated_pwd)
                print("Password:", generated_pwd)
                print("Password copied to clipboard")
                print()
                choice = input(
                    "Do you want to store this password? (y/n): ").lower()
                if choice == 'y':
                    cliearscr()
                    website = input("Enter Website: ")
                    username = input("Enter Username: ")
                    password = generated_pwd
                    database.storepwd(database_path, website,
                                      username, password)
                else:
                    print("Password not stored.....")

            elif option == 's':
                cliearscr()
                website = input("Enter Website: ")
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                database.storepwd(database_path, website, username, password)

            elif option == 'f':
                cliearscr()
                # find by website or username
                findby = input(
                    "Find Password by (w)ebsite or (u)sername: ").lower()
                database.findpwd(database_path, findby)

            elif option == 'c':
                cliearscr()
                database.changepwd(database_path)

                cliearscr()
                print("Password changed successfully")
                print("Updated table:")
                database.printall(database_path)

            elif option == 'd':
                cliearscr()
                # deleteby one or delete all
                deleteby = input("delete (o)ne or (a)ll: ").lower()
                if deleteby == 'o':
                    database.deletepwd(database_path)
                    cliearscr()
                    database.printall(database_path)

                elif deleteby == 'a':
                    database.deletedb(database_path)
                    cliearscr()
                    print("All passwords deleted successfully")
                    print("Removing database file from the system")
                    os.remove(database_path)
                    choice = input(
                        "Do you want to create a new database? (y/n): ").lower()
                    if choice == 'y':
                        database.createdb(database_path)
                        cliearscr()
                        print("New database created successfully")
                    else:
                        sys.exit("Quiting the program....")

            elif option == 'a':
                cliearscr()
                database.printall(database_path)
