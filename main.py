from interface import menu
from master_password import verify_masterpwd, create_masterpwd
import sys
from os.path import exists

hash_file_path = "password_hash.argon2"  # password hash file path


# main function
def main():
    try:
        # check if password_hash file that contains hash exists or not
        if exists(hash_file_path):  # if exits then try to match it
            tried_count = 3
            while True:
                tried_count -= 1
                verified = verify_masterpwd(hash_file_path)
                if verified == True:    # if password is verified then break from loop
                    break
                elif tried_count == 0:  # if failed for 3 times exit
                    sys.exit("Too many Tries. Exiting the program...")
                else:
                    print("Wrong Password")

        else:
            create_masterpwd(hash_file_path)

        menu()

    except (KeyboardInterrupt, EOFError):   # handles Ctrl + c and Ctrl + d
        sys.exit("Quitted Prematurely")


if __name__ == "__main__":
    main()
