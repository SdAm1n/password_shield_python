# AES Key generation from password so that
# we do not need to save it to a disk

from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.PublicKey import RSA


# generate AES key from password
def aes_key(password):

    # 32 for AES 256 bit --> 256/8 bit = 32 byte
    # print(get_random_bytes(32))

    # TODO: generate a random salt or use it from a file or something ?
    salt = b'\xe9\xbb\x84\xdcu}$\x97\xe4@\\i\xb1`t\xf0\xcb\xcc\x93\xeaTc(q\x88\xf5\xcf\x900\xf2.\x96'

    # AES KEY
    key = PBKDF2(password, salt, dkLen=32)  # 32 for AES 256

    return key


def rsa_key():

    # RSA.generate(bits, randfunc=None, progress_func=None, e=65537)
    key = RSA.generate(2048)

    # RSA private key
    private_key = key.export_key()

    # saves the private key to a file
    with open("private.pem", "wb") as file:
        file.write(private_key)

    # RSA public key
    public_key = key.public_key().export_key()

    # saves the public key to a file
    with open("receiver.pem", "wb") as file:
        file.write(public_key)
