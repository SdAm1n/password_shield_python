"""
This file contains the functions to encrypt and decrypt the password using RSA and AES.
First RSA Public Key is used to encrypt the AES session key and then AES is 
used to encrypt the password.
RSA Private Key and the encrypted AES session key is used to decrypt the Password.
"""

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from masterpwd import get_aes


# --------------- Encrypt The Data -------------------
def encryptpwd(password):

    recipient_key = RSA.import_key(open("receiver.pem").read())
    session_key = get_aes()

    # Encrypt the session key with public rsa key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(password)

    return enc_session_key, cipher_aes.nonce, tag, ciphertext


# --------------- Decrypt The Data -------------------
def decryptpwd(enc_session_key, nonce, tag, ciphertext):

    private_key = RSA.import_key(open("private.pem").read())

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    password = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return password.decode("utf-8")
