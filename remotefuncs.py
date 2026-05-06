#remotefuncs.py
import hashlib,os, json,base64,getpass
from cryptography.fernet import Fernet
import asyncio, websockets
import websockets
import random
def sha(x):
    return hashlib.sha256(x.encode()).digest()

def baseify(x):
    return base64.urlsafe_b64encode(x)
class attr:
    password: str| bytes= "default"
    username:  str | bytes = "default"
    messages = {"ls":"os.listdir()", "pwd":"os.getcwd()", "cat":"open(args).read()"}
    logged=False
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
        
# remotefuncs.py - Update these parts:

async def serverlogin(websocket, message): # Add websocket here
    try:    
        # No need for nested 'async def login' anymore
        nonce = str(random.randint(100000, 999999))
        await websocket.send(nonce) # Use the passed connection object
        
        cr = await websocket.recv()
        # Decode if it's bytes, then strip and split
        if isinstance(cr, bytes): cr = cr.decode()
        cr_parts = cr.strip().replace("|", "").split()
        
        # Simple check for testing
        if len(cr_parts) > 0 and baseify(sha(cr_parts[0])).decode() in os.listdir():
            await websocket.send("ok")
            attr.logged = True
            return "Auth Successful"
        else:
            await websocket.send("Auth Failed")
            return "Auth Failed"
            
    except Exception as e:
        print(f"Login error: {e}")