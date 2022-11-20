import secrets
import base64
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import hashlib

"""resources on this page found at thepythoncode.com"""  


def hash(input: str):
    h = hashlib.sha3_256(input.encode())
    return h.hexdigest()

def generate_salt(size=16):
    """Generate the salt used for key derivation,
    'size' is the length of the salt to generate"""
    return secrets.token_bytes(size)

def derive_key(salt, password):
    """Derive the key from the 'password' using the passed 'salt'"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()

def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """
    Generates a key from a 'password' and the salt.
    If 'load_existing_salt' is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If 'save_salt' is True, then it will generate a new salt
    and save it to "salt.salt"
    """
    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)

    derived_key = derive_key(salt, password)

    return base64.urlsafe_b64encode(derived_key)

def encrypt(filename, key):
    """
    Given a filename(str) and key(bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """
    Given a filename(str) and key(bytes), it decrypts the file and writes it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect.")
        return
 
    with open(filename, "wb") as file:
        file.write(decrypted_data)

