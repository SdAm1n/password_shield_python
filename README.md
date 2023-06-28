# Password Shield in Python

## TODO

- [x] Design Menu
  - [ ] Make Menu Beautiful
  - [ ] Handle Ctrl + z
- [x] Hash Master Password with Argon2
  - [ ] password masking
  - [ ] Add more functionality
  - [ ] secure the hash file
- [x] Generate Password
  - [ ] advance password generation
  - [ ] Save generated password to database option
- [x] Setup Database with sqlite3
- [x] Encrypt Password
  - [x] RSA Implementation
  - [x] AES Implementation
  - [x] Hybrid Implementation
- [x] Setup 2FA
- [ ] Auto copy Password
- [x] Encrypt the Generated Keys
- [ ] Store the keys (give user the option?)
- [x] Encrypt whole Database with pysqlcipher3

## Important Note

- Create a branch (e.g. dev) then edit and push that branch
- Only i will merge to the main branch
- And obviously do not make the repo public
- Add any file in .gitignore if you want it to be ignored

## How to run

- first you need to install libsqlcipher-dev for sqlite3 encryption to work

```bash
# for debian based distros
sudo apt install libsqlcipher-dev
# for arch based distros install from the AUR
paru libqsqlcipher
```

- Then install the requirements.txt and run the main.py file

```bash
pip install -r requirements.txt
python main.py
```
