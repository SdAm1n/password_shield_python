"""
This file contains the functions to encrypt and decrypt files using AES.
"""

from masterpwd import get_aes
from Cryptodome.Cipher import AES
import os


def encrypt_file(file_path):

    # print("Encrypting File...")

    key = get_aes()

    # Create an AES cipher object
    cipher = AES.new(key, AES.MODE_EAX)

    # Open the RSA public key file
    with open(file_path, "rb") as file:
        # Read the public key data
        data = file.read()
        # Encrypt the data and get the nonce and tag
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        # Write the nonce, tag, and ciphertext to a new file
        with open(f"{file_path}.encrypted", "wb") as enc_file:
            for x in (nonce, tag, ciphertext):
                enc_file.write(x)

    # print("Successfully Encrypted File...")
    # print("Deleting Original File...")
    os.remove(file_path)


def decrypt_file(file_path):

    # print("Decrypting File...")

    key = get_aes()

    # Open the encrypted RSA private key file
    with open(f"{file_path}.encrypted", "rb") as enc_file:
        # Read the nonce, tag, and ciphertext from the file
        nonce, tag, ciphertext = [
            enc_file.read(x) for x in (16, 16, -1)]
        # Create an AES cipher object with the nonce
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        # Decrypt the data and verify the tag
        data = cipher.decrypt_and_verify(ciphertext, tag)
        # Write the decrypted data to a new file
        with open(file_path, "wb") as priv_file:
            priv_file.write(data)

    # print("Successfully Decrypted File...")
    # print("Deleting Encrypted File...")
    os.remove(f"{file_path}.encrypted")
