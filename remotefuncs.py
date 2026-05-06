#remotefuncs.py
import hashlib,os, json,base64,getpass,asyncio, websockets,random
from cryptography.fernet import Fernet

def sha(x):
    return hashlib.sha256(x.encode()).digest()
def shasafe(x):
    return hashlib.sha256(x.encode()).hexdigest()
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

# remotefuncs.py

# REMOVE: from fastapi import websockets
# KEEP: import websockets

async def serverlogin(websocket, message): # Accept the connection object
    try:    
        # Generate the random nonce for the UC66 handshake
        nonce = str(random.randint(100000, 999999)) 
        await websocket.send(nonce) 
        
        # Receive the combohash from the client
        cr = await websocket.recv()
        
        # Basic cleanup of the received string
        if cr ==baseify(sha('Nt5SeyrdEyxqwuzdtbGiM6DsDAwceLwa6JYQK8qhB3Q=' + str(nonce))).decode():
            websocket.send("Login successful!")
            print("Client authenticated successfully.")
    except Exception as e:
        print(f"Login error: {e}")
        return "Error"