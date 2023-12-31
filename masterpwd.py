"""
This file contains functions for creating and verifying master password by using argon2id.
This file also contains functions for generating and verifying otp.
This file also contains functions for generating rsa and aes keys.
this file also contains functions for changing master password and rehashing master password if needed.
this file also contains functions for getting aes key and master password.
"""

import argon2
import sys
import pwinput
from keygen import aes_key, rsa_key
from os.path import exists
from twoFA import generate_otp, verify_otp


# function for initializing argon2id
def init(tc=3, mc=488281, p=4, hl=32):
    global ph
    ph = argon2.PasswordHasher(
        time_cost=tc, memory_cost=mc, parallelism=p, hash_len=hl)


# verify otp when the user tries to login
def verify_twoFA(master_pwd):
    otp_count = 5
    while True:
        otp_count -= 1
        # verify otp when the user tries to login
        if verify_otp(master_pwd) == True:
            break
        elif otp_count == 0:
            sys.exit("Too many Tries. Exiting the program...")


# func for generating hash value using argon2id
def generate_hash(master_pwd):
    # modified the memory cost parameter and kept everything default
    try:
        hash = ph.hash(master_pwd)
    except argon2.exceptions.HashingError:
        sys.exit("Hashing Failed")
    else:
        return hash


# verify a password hash
def verify_masterpwd(hash_file_path):

    global master_pwd
    master_pwd = pwinput.pwinput(prompt="Enter Master Password: ", mask='*')
    # match the hash value with the file hash value
    init()  # initialize argon2id
    with open(hash_file_path, 'r') as file:
        try:
            ph.verify(file.read(), master_pwd)
        except argon2.exceptions.VerifyMismatchError:
            return False
        else:
            if not exists("qrcode.png"):
                # generate otp and generate qr code from it only once when the user creates the master password
                generate_otp(master_pwd)

            verify_twoFA(master_pwd)  # verify otp when the user tries to login

            # generate aes key and assign it to aeskey
            global aeskey
            aeskey = aes_key(master_pwd)

            if not exists("private.pem.encrypted") or not exists("receiver.pem.encrypted"):
                # if the user quits before entering the master password
                sys.exit(
                    "Private key or Public key is missing. Exiting the program...")
            return True


# create a password hash and save it to file
def create_masterpwd(hash_file_path):
    print("Do you want to use default parameters or advanced parameters?")
    user_choice = input("(D) efault or (A) dvanced?: ").lower()

    # if the file does not exist ask for new master password
    # then genereate a new hash
    print("You need to create a Master Password to continue.")
    print("Remember if you loose your master password, everything will be lost")
    global master_pwd
    master_pwd = pwinput.pwinput(prompt="Enter Master Password: ", mask='*')

    if (user_choice == "d"):
        init()  # initialize argon2id
        hash = generate_hash(master_pwd)    # hash value

    elif (user_choice == "a"):
        print("Enter the following parameters to generate a hash value")
        tc = int(input("Time Cost: "))
        mc = int(input("Memory Cost: "))
        p = int(input("Parallelism: "))
        hl = int(input("Hash Length: "))
        init(tc, mc, p, hl)  # initialize argon2id
        hash = generate_hash(master_pwd)    # hash value

    else:
        print("Invalid Choice. Exiting the program...")
        sys.exit()

    with open(hash_file_path, "w") as file:  # write hash value to file
        file.write(hash)
    print("Master Password created successfully")

    # generate otp and generate qr code from it only once when the user creates the master password
    generate_otp(master_pwd)

    # verify otp when the user creates the master password
    verify_twoFA(master_pwd)

    print("Generating AES key...")
    global aeskey
    aeskey = aes_key(master_pwd)    # generate aes key and assign it to aeskey
    print("AES key generated successfully")

    print("Generating RSA key...")
    rsa_key()   # generate rsa key
    print("RSA key generated successfully")


def get_aes():
    return aeskey


def get_masterpwd():
    return master_pwd


# change master password
def change_masterpwd():
    ...


# rehash master password if needed
def rehash_masterpwd():
    ...
