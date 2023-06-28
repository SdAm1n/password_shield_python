import argon2
import sys
from keygen import aes_key, rsa_key
from os.path import exists


ph = argon2.PasswordHasher(memory_cost=488281)


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

    master_pwd = input("Enter Master Password: ")
    # match the hash value with the file hash value
    with open(hash_file_path, 'r') as file:
        try:
            ph.verify(file.read(), master_pwd)
        except argon2.exceptions.VerifyMismatchError:
            return False
        else:
            # generate aes key and assign it to aeskey
            aeskey = aes_key(master_pwd)
            if not exists("private.pem") or not exists("public.pem"):
                rsa_key()   # generate rsa key
            return True


# create a password hash and save it to file
def create_masterpwd(hash_file_path):
    # if the file does not exist ask for new master password
    # then genereate a new hash
    print("You need to create a Master Password to continue.")
    print("Remember if you loose your master password, everything will be lost")
    master_pwd = input("Enter Master Password: ")
    hash = generate_hash(master_pwd)    # hash value
    with open(hash_file_path, "w") as file:  # write hash value to file
        file.write(hash)
    print("Master Password created successfully")

    print("Generating AES key...")
    aeskey = aes_key(master_pwd)    # generate aes key and assign it to aeskey
    print("AES key generated successfully")

    print("Generating RSA key...")
    rsa_key()   # generate rsa key
    print("RSA key generated successfully")


# change master password
def change_masterpwd():
    ...


# rehash master password if needed
def rehash_masterpwd():
    ...
