import json
import encryption
import getpass

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
        json.dump(data, f, indent=4)


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
                elif ans == "2":
                    entry["Username"] = input("New username: ")
                elif ans == "3":
                    entry["Password"] = input("New password: ")
                else:
                    print("Response not understood. No changes made.")
                break 
        if found:
            encryption.write_to_json_file(database, password, data)
            input("Changes made!")
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
            ans1 = input("Would you like to search for another Profile? (Y/N) ")
            if ans1 == "Y":
                continue
            elif ans1 == "N":
                exit = True
                break
            else:
                input("Didn't understand input. Press any key to return to main menu.")
                return
        elif not found:
            ans2 = input("It looks like either the name was mistyped or your website has no Profile in the database yet. Would you like to start another search? (Y/N) ")
            if ans2 == "Y":
                continue
            elif ans2 == "N":
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

    for i in range(len(entries)):
        if entries[i]["Name"].lower() == target.lower():
            del entries[i]
            break
        else:
            pass

    encryption.write_to_json_file(database, password, data)

    input("Profile removed.")



def changeMasterPassword(password):
    return

def deleteDatabase(password):
    return


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


    #BOOKMARK: create db empty textfile and encrypt
    with open(database, "w") as database_file:
        json.dump(json.loads(modelOfJSON), database_file)

    encryption.encrypt(database, key)

    del key

    print("Database created with Master Password! Don't forget it!")

def verify_master(hashed_input):

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
    else:
        del master
        del hashed_input
        return False