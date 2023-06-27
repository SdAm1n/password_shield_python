# a simple menu function
def menu():
    # calling until user quits
    while True:
        print("MENU")
        print("-----------------")
        print("(G)enearate Password")
        print("(S)tore Password")
        print("(F)ind Password")
        print("(C)hange Password")
        print("(D)elete")
        print("(A)ll Password")
        print("(Q)uit")
        try:
            option = input("Enter Choice: ")
        except ValueError:  # if user inputs invalid Choice
            print("Enter a valid Choice: ")
        else:
            if option == 'Q' or option == 'q':
                break
