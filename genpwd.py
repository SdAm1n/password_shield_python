"""
This module generates a random secure password
"""

import secrets
import string


# generate random password
def generatepwd():

    # ask user password size
    password_size = int(input("Password length: "))

    print("Generating Password....................\n")

    alphabet = string.ascii_letters + string.digits + string.punctuation

    # makes sure a lower case, an upper case char
    # and a digit is in password
    while True:
        password = "".join(secrets.choice(alphabet)
                           for i in range(password_size))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
            return password


# advance password generation
def advance_generatepwd():
    ...
