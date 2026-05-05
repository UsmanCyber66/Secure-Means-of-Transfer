#remotefuncs.py
import hashlib,os, json,base64,getpass
from cryptography.fernet import Fernet

from fastapi import websockets

def sha(x):
    return hashlib.sha256(x.encode()).digest()

def baseify(x):
    return base64.urlsafe_b64encode(x)
class attr:
    password: str| bytes= "default"
    username:  str | bytes = "default"
    messages = {"ls":"os.listdir()", "pwd":"os.getcwd()", "cat":"open(args).read()"}
    @classmethod
    def get_key(cls):
        # This calculates the key "on the fly" using the CURRENT password
        return baseify(sha(cls.password))

def encrypt(data) :
    f = Fernet(attr.get_key())
    return f.encrypt(data.encode())

def byte(file):
    with open(file, "rb") as f:
        return f.read() 
def get(x):
    try:    
        with open(x, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        return "File not found."
def inpute(prompt):
    while True:
        value = input(prompt).strip()
        if value:  # This checks if the string is NOT empty
            return value
        print("Input cannot be empty. Please try again.")
        
def getepass(prompt="Enter Password: "):
    while True:
        # getpass hides the typing in the terminal
        pw = getpass.getpass(prompt)
        if pw.strip():  # Ensures it's not empty or just spaces
            return pw
        print("Password cannot be empty!")
        
def serverlogin(message):
    x= message.strip().strip("|")
    u = baseify(sha(x[0])).decode()
    if os.path.exists(u) == True:
        with open(u, "r") as f:
            data = json.load(f)
        if data["combohash"] == baseify(sha(u + x[1])).decode(): 
            print("User authenticated successfully.")
        else:
            print("Authentication failed: combohash error")
    else:
        print("Authentication failed: user not found")
        