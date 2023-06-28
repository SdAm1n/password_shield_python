"""
This file contains the functions to generate and verify OTP using pyotp and qrcode
"""

import pyotp
import qrcode
from PIL import Image
import base64


# get master password from user to use it as the key for google authenticator
def get_key(master_password):

    # TODO: get key from user or something (most probably from master password not sure) ??
    # convert to base32
    key = base64.b32encode(bytearray(master_password, 'ascii')).decode('utf-8')
    return key

# key = "$argon2id$v=19$m=488281,t=3,p=4$xIzd96Z+NaVJ0e7+EjF8sQ$/s5BNmi9up5/XfCRiPSFsJTD3s/GI6m9mPQTVC5MDfE"
# print(key)


# generate otp and generate qr code from it only once when the user creates the master password
def generate_otp(master_password):
    # create uri for google authenticator
    key = get_key(master_password)
    user_name = input("Enter Your name: ")
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=user_name,
                                                issuer_name="Password Shield")
    # make image and save image from uri
    image_name = "qrcode.png"
    qrcode.make(uri).save(image_name)

    # open and show image using pillow
    img = Image.open(image_name)
    img.show()
    print("Scan the QR code using Google Authenticator App")


# verify otp when the user tries to login
def verify_otp(master_password):
    # match the OTP
    key = get_key(master_password)
    totp = pyotp.TOTP(key)

    # return true if otp matches
    return totp.verify(input("Enter OTP: "))
