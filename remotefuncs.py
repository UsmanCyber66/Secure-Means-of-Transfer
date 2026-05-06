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
    users = []
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
        if cr ==baseify(sha('Nt5SeyrdEyxqwuzdtbGiM6DsDAwceLwa6JYQK8qhB3Q=' + str(nonce))).decode().encode("utf-8"):
            await websocket.send("Login successful!")
            print("Client authenticated successfully.")
    except Exception as e:
        print(f"Login error: {e}")
        return "Error"
    
import ast

def update_persistent_list(new_username):
    file_path = "remotefuncs.py"
    
    # 1. Read the current contents
    with open(file_path, "r") as f:
        lines = f.readlines()

    # 2. Write the updated contents
    with open(file_path, "w") as f:
        # enumerate starts at 1 to match human line numbers
        for line_num, line_content in enumerate(lines, 1):
            
            # Target line 16 (where your 'users = []' is)
            if line_num == 16:
                if "users =" in line_content:
                    # Extract the list part after the '='
                    parts = line_content.split("=")
                    current_list_str = parts[1].strip()
                    
                    try:
                        current_list = ast.literal_eval(current_list_str)
                    except Exception:
                        current_list = []
                    
                    # Add user if not already there
                    if new_username not in current_list:
                        current_list.append(new_username)
                    
                    # Write the updated line (keeping the 4-space indent)
                    f.write(f"    users = {current_list}\n")
                else:
                    # If line 16 isn't what we thought, just write it back
                    f.write(line_content)
            else:
                # Write back every other line exactly as it was
                f.write(line_content)