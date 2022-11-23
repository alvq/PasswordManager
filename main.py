#Create a random password generator!

import os
import getpass
import encryption
import database as db
from time import sleep

#TODO
#Loop password entry on failure, possibly limit amount of loopsk

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
 
    for attempts in range(3):
        print("WELCOME TO LOCKIT\n\n\n\n")
        hashed_pass = encryption.hash(getpass.getpass("Enter the correct Master Password: "))
        if db.verify_master(hashed_pass):
            print("\n\nLoading...")
            sleep(1)
            mainMenu(hashed_pass)
            del hashed_pass
            return
        else:
            input("Wrong password. Press enter to try again.")
            cls()
    print("Too many failed attempts. Quitting..")
    sleep(1)
    cls()
    
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
            db.deleteProfile(hashed_pass)
        elif response == "6":
            db.deleteDatabase()
        elif response == "7":
            hashed_pass = db.changeMasterPassword()
        else:
            cls()
            print("Response not understood. Stop messing around.")
            input()
            cls()
    return

if __name__ == "__main__":
    main()