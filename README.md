# Password Shield in Python
## This is an Experimental Project

Password Shield is a password manager using AES, RSA, PBKDF2, and Argon2 algorithms. This is a highly experimental project to test out the capabilities of a password manager and what one can do with these various algorithms and technologies. Google Authenticator app is used for two-factor authentication. Sqlite3 was chosen as it was lightweight and easy to implement. Used many Python libraries like Pycryptodome for encryption algorithms, Pysqlcipher for encrypting databases, Argon2 for argon2id hashing algorithms, Pillow for qrcode image generation, and  Secrets for generating random passwords cryptographically.

## TODO

- [x] Design Menu
  - [ ] Make Menu Beautiful
  - [ ] Handle Ctrl + z
- [x] Hash Master Password with Argon2
  - [ ] Add more functionality
  - [ ] secure the hash file
- [x] password masking
- [x] Generate Password
  - [x] Save generated password to database option
  - [ ] advance password generation
- [x] Setup Database with sqlite3
- [x] Encrypt Password
  - [x] RSA Implementation
  - [x] AES Implementation
  - [x] Hybrid Implementation
- [x] Setup 2FA
- [x] Auto copy Password
- [x] Encrypt the Generated Keys
- [x] Encrypt the encrypted data with RSA
- [x] Encrypt whole Database with pysqlcipher3


## How to run

- first you need to install libsqlcipher-dev for sqlite3 encryption to work

```bash
# for debian based distros
sudo apt install libsqlcipher-dev
# for arch based distros install from the AUR
paru libqsqlcipher
```

- Then install xclip for auto copying password

```bash
# for arch based distros
sudo pacman -Syu xclip
```

- Finally install the requirements.txt and run the main.py file

```bash
pip install -r requirements.txt
python main.py
```
