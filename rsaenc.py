"""
This module contains the functions for RSA encryption and decryption.
"""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


def rsa_keygen():
    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open("private2.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("receiver2.pem", "wb")
    file_out.write(public_key)
    file_out.close()


def rsa_encrypt(data):

    public_key = RSA.import_key(open("receiver2.pem").read())
    cipher = PKCS1_OAEP.new(public_key)

    # Encrypt the message using the cipher object
    ciphertext = cipher.encrypt(data)

    # # Return the encrypted message as bytes
    return ciphertext


def rsa_decrypt(ciphertext):

    private_key = RSA.import_key(open("private2.pem").read())

    # Create another cipher object using the private key
    cipher = PKCS1_OAEP.new(private_key)

    # Decrypt the ciphertext using the cipher object
    plaintext = cipher.decrypt(ciphertext)

    return plaintext
    # # Print the decrypted message
    # print(plaintext.decode())
