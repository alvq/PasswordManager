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

def write_json(data, filename=database):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


#takes in database and hashed password and displays all data in database from copy
def viewDatabase(mPassword):
    data = json.loads(encryption.get_data(database, mPassword))
    stuff = data["profiles"]
    i = 0
    for entry in stuff:
        name = entry["Name"]
        username = entry["Username"]
        password = entry["Password"]
        print(f"i: {i}")
        print(f'Website : {name}')
        print(f'Username: {username}')
        print(f'Password: {password}\n\n')
        i = i+1
    input("Enter any key to exit: ")
    del stuff
    del data
    return

def editProfile(password):
    return


#TODO
#ADD SEARCH TO SEE IF ALREADY IN DATABASE

def addProfile(password):
    newProfile = {}
    newProfile["Name"] = input("Enter the name of the website for this profile: ")
    newProfile["Username"] = input("Enter the username: ")
    newProfile["Password"] = input("Enter the password: ")

    data = json.loads(encryption.get_data(database, password))
    temp = data["profiles"]
    temp.append(newProfile)    

    encryption.write_to_json_file(database, password, data)
    del data
    del temp
    return

def findProfile(password):
    exit = False
    data = json.loads(encryption.get_data(database, password))
    entries = data["profiles"]
    while not exit:
        found = False
        profileSearch = input("What is the name of the website for the Profile you want to see: ")
        for entry in entries:
            if entry["Name"] == profileSearch:
                found = True
                name = entry["Name"]
                username = entry["Username"]
                password = entry["Password"]
                print("Profile found!\n")
                print(f'Website : {name}')
                print(f'Username: {username}')
                print(f'Password: {password}\n\n')
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

def deleteProfile():
    return


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