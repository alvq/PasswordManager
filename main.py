#Create a random password generator!

import os
import secrets
import getpass
import encryption
import database as db
from time import sleep


def cls(): os.system('cls' if os.name == 'nt' else 'clear')

def main():
    #Test to see if profile exists
    #Create profile or show main menu
    try:
        fp = open(db.database, "r+")
        fp.close()
    except:
        print("Database file not in directory...proceeding to Database Creation.\n")
        sleep(1)
        db.database_setup()
        sleep(1)
    cls()
    print("WELCOME TO LOCKIT  \n\n\n\n")
    hashed_pass = encryption.hash(getpass.getpass("Enter the correct Master Password: "))

    try:
        db.verify_master(hashed_pass)
        print("\n\nLoading...")
        sleep(2)
        mainMenu(hashed_pass)
        del hashed_pass
    except:
        print("Something went wrong. Goodbye.")
    
def mainMenu(hashed_pass):
    cls()
    loop = True
    while loop:
        cls()
        print("WELCOME TO LOCKIT!\n\nYour personal password manager! \n\n")
        print("1. View database")
        print("2. Add Profile")
        print("3. Find Profile")
        print("4. Edit Profile")
        print("5. Delete Profile")
        print("6. Delete Database")
        print("7. Change Master Password")
        print("0. Exit\n\n")

        response = input("Please select an option: ")
        cls()
        if response == "0":
            loop = False
            print("Goodbye.")
            break
        elif response == "1":
            db.viewDatabase(hashed_pass)
        elif response == "2":
            db.addProfile(hashed_pass)
        elif response == "3":
            db.findProfile(hashed_pass)
        elif response == "4":
            db.editProfile(hashed_pass)
        elif response == "5":
            db.deleteProfile()
        elif response == "6":
            db.deleteDatabase(hashed_pass)
        elif response == "7":
            db.changeMasterPassword(hashed_pass)
        else:
            cls()
            print("Response not understood. Stop messing around.")
            input()
            cls()
    return

def generatePassword(size=12):
    #gather our characters
    if size < 8:
        size = 12

    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    symbols = '!@#$%^&*()_+-=[]\{}|;:,./<>?'
    numbers = '1234567890'

    all = lower + upper + symbols + numbers

    #loop through each character
    password = ''
    for i in range(size):
        password = ''.join([password, secrets.choice(all)])

    return password


if __name__ == "__main__":
    main()