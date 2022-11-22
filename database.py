import json
import encryption
import getpass
import os

database = "MAINDATABASE.json"
modelOfJSON = """
{ 
    "profiles":[
    ]
}
"""
def print_dict(data):
    print(f'Website : {data["Name"]}')
    print(f'Username: {data["Username"]}')
    print(f'Password: {data["Password"]}\n')

def write_json(data, filename=database):
    with open(filename, "w") as f:
        json.dump(data, f)


#takes in database and hashed password and displays all data in database from copy
def viewDatabase(mPassword):
    data = json.loads(encryption.get_data(database, mPassword))
    entries = data["profiles"]
    i = 0
    for entry in entries:
        print(f"i: {i}")
        print_dict(entry)
        i = i+1
    input("Enter any key to continue: ")
    del entries
    del data
    return

def editProfile(password):
    data = json.loads(encryption.get_data(database, password))
    entries = data["profiles"]
    found = False
    target = input("What website would you like to edit? ")
    while not found:
        for entry in entries:
            if entry["Name"].lower() == target.lower():
                found = True
                print_dict(entry)
                print("Which would you like to change?\n1. Domain name  2. Username  3. Password")
                ans = input()
                if ans == "1":
                    entry["Name"] = input("New domain name: ")
                    input("Changes made!")
                elif ans == "2":
                    entry["Username"] = input("New username: ")
                    input("Changes made!")                    
                elif ans == "3":
                    entry["Password"] = input("New password: ")
                    input("Changes made!")                    
                else:
                    print("Response not understood. No changes made.")
                break 
        if found:
            encryption.write_to_json_file(database, password, data)
            del data, entries
            return
        elif not found:
            input("Couldn't find that profile in the database! No changes made. Return to main menu.")
            del data, entries
            return
        else:
            input("idk what happened tbh")
            return


#TODO
#ADD SEARCH TO SEE IF ALREADY IN DATABASE - Done.11/22/22

def addProfile(password):
    data = json.loads(encryption.get_data(database, password))
    entries = data["profiles"]

    newProfile = {}
    newProfile["Name"] = input("Enter the name of the website for this profile: ")

    for entry in entries:
        if entry["Name"] == newProfile["Name"]:
            input("Profile already exists for this website! Returning to main menu.")
            return

    newProfile["Username"] = input("Enter the username: ")
    newProfile["Password"] = input("Enter the password: ")


    entries.append(newProfile)
    encryption.write_to_json_file(database, password, data)

    del data
    del entries
    return

def findProfile(password):
    exit = False
    data = json.loads(encryption.get_data(database, password))
    entries = data["profiles"]
    while not exit:
        found = False
        profileSearch = input("What is the name of the website for the Profile you want to see: ")
        for entry in entries:
            if entry["Name"].lower() == profileSearch.lower():
                found = True
                print("Profile found!\n")
                print_dict(entry)
                break

        if found:
            ans1 = input("Would you like to search for another Profile? (Y/N) ").lower()
            if ans1 == "y":
                continue
            elif ans1 == "n":
                exit = True
                break
            else:
                input("Didn't understand input. Press any key to return to main menu.")
                return
        elif not found:
            ans2 = input("It looks like either the name was mistyped or your website has no Profile in the database yet. Would you like to start another search? (Y/N) ").lower()
            if ans2 == "y":
                continue
            elif ans2 == "n":
                exit = True
                break
            else:
                input("Didn't understand input. Press any key to return to main menu.")
                return
    del data
    del entries
    return

def deleteProfile(password):
    viewDatabase(password)
    data = json.loads(encryption.get_data(database, password))
    entries = data["profiles"]
    
    target = input("Which website would you like to remove: ")
    deleted = False
    for i in range(len(entries)):
        if entries[i]["Name"].lower() == target.lower():
            deleted = True
            del entries[i]
            break
        else:
            pass
    if deleted:
        encryption.write_to_json_file(database, password, data)
        input("Profile removed.")
    else:
        input("Profile not found in database to remove. Returning to main menu.")

def deleteDatabase():
    print("DATABASE WIPE SETTINGS\n\n")
    prompt = input("Are you sure you want to wipe the database? (Yes/No) ")
    if prompt.lower() == "yes":
        test = getpass.getpass("\nEnter your master password: ")
        hashed_test = encryption.hash(test)
        if verify_master(hashed_test):
            data = json.loads(encryption.get_data(database, hashed_test))
            entries = data["profiles"]            
            for i in range(len(entries)-1):
                del entries[i]
            encryption.write_to_json_file(database, hashed_test, data)
            input("Database wiped!")
        else:
            input("Get out of here!")
            os.system('cls')
            quit()    
    elif prompt.lower() == "no":
        input("That's what I thought!")
    return

def changeMasterPassword():
    print("MASTER PASSWORD SETTINGS\n\n")
    prompt = input("Are you sure you want to change your master password? (Yes/No) ")
    if prompt.lower() == "yes":
        test = getpass.getpass("\nEnter your current master password: ")
        hashed_test = encryption.hash(test)
        if verify_master(hashed_test):
            #decrypt database to reencrypt it with the new password
            oldkey = encryption.generate_key(hashed_test, load_existing_salt=True, save_salt=False)
            encryption.decrypt(database, oldkey)
            del test
            loop = True
            while loop:
                new_master_pass = getpass.getpass("Enter your new master password: ")
                test_input = getpass.getpass("Reenter the password to confirm: ")
                if new_master_pass == test_input:
                    new_master_pass_HASHED = encryption.hash(new_master_pass)
                    del new_master_pass, test_input
                    loop = False
                    with open("VERIFIER.txt", "w") as file:
                        file.write(new_master_pass_HASHED)
                    key = encryption.generate_key(new_master_pass_HASHED)
                    encryption.encrypt("VERIFIER.txt", key)
                    encryption.encrypt(database, key)
                    input("\n\nMaster password changed. Don't forget your new password!")
                    del key
                    return new_master_pass_HASHED
                else:
                    cont =input("Passwords did not match. Press enter to try again or 0 to exit.")
                    if cont == "0":
                        #passwords werent changed, encrypting file before exit
                        encryption.encrypt(database, oldkey)
                        del oldkey
                        loop = False
                    else:
                        pass
        else:
            input("Incorrect master password, get out of here.")
            os.system('cls')
            quit()
    elif prompt == "n":
        input("That's what I thought!")

def database_setup():
    """
    Sets up database and files for first time use
    """
    print("DATABASE CREATION\n\n")
    plain_text_password = getpass.getpass("What would you like to set as your Master Password: ")
    hashed_pass = encryption.hash(plain_text_password)
    del plain_text_password

    with open("VERIFIER.txt", "w") as file:
        file.write(hashed_pass)
    
    key = encryption.generate_key(hashed_pass)
    encryption.encrypt("VERIFIER.txt", key)
    del hashed_pass

    write_json(json.loads(modelOfJSON), database)

    encryption.encrypt(database, key)

    del key

    print("Database created with Master Password! Don't forget it!")

def verify_master(hashed_input):

    try:
        key = encryption.generate_key(hashed_input, load_existing_salt=True, save_salt=False)
        encryption.decrypt("VERIFIER.txt", key)

        with open("VERIFIER.txt", "r") as file:
            master = file.read()

        encryption.encrypt("VERIFIER.txt", key)
        del key

        if hashed_input == master:
            del master
            del hashed_input
            return True
    except:
        del hashed_input
        return False