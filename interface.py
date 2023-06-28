from genpwd import generatepwd
import os
import sys
import database


database_path = "password_list.db"


# to clear terminal
def clearscr():
    if os.name == "nt":     # for detecting windows operating system
        os.system("cls")
    else:                   # for detecting linux/mac (os.name == "posix")
        os.system("clear")


# a simple menu function
def menu():
    # calling until user quits
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
                sys.exit("Quiting the program....")

            elif option == 'g':
                clearscr()
                generated_pwd = generatepwd()
                print("Password:", generated_pwd)
                print()

            elif option == 's':
                clearscr()
                website = input("Enter Website: ")
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                database.storepwd(database_path, website, username, password)

            elif option == 'f':
                clearscr()
                # find by website or username
                findby = input(
                    "Find Password by (w)ebsite or (u)sername: ").lower()
                database.findpwd(database_path, findby)

            elif option == 'c':
                clearscr()
                database.changepwd(database_path)

                clearscr()
                print("Password changed successfully")
                print("Updated table:")
                database.printall(database_path)

            elif option == 'd':
                clearscr()
               # deleteby one or delete all
                deleteby = input("delete (o)ne or (a)ll: ").lower()
                if deleteby == 'o':
                    database.deletepwd(database_path)
                    clearscr()
                    database.printall(database_path)

                elif deleteby == 'a':
                    database.deletedb(database_path)
                    clearscr()
                    print("All passwords deleted successfully")
                    print("Removing database file from the system")
                    os.remove(database_path)
                    choice = input(
                        "Do you want to create a new database? (y/n): ").lower()
                    if choice == 'y':
                        database.createdb(database_path)
                        clearscr()
                        print("New database created successfully")
                    else:
                        sys.exit("Quiting the program....")

            elif option == 'a':
                clearscr()
                database.printall(database_path)
