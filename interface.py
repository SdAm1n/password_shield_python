from generate_password import generatepwd
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
            elif option == 'a':
                database.printall(database_path)
