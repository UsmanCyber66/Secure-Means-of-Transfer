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
    users = ['Nt5SeyrdEyxqwuzdtbGiM6DsDAwceLwa6JYQK8qhB3Q=']
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
        for i in attr.users:
            if noncify(i, nonce) == cr:
                attr.logged = True
                await websocket.send("Login successful!")
                print("Client authenticated successfully.")
                break
        else:
            await websocket.send("Login failed!")
    except Exception as e:
        print(f"Login error: {e}")
        return "Error"
    
import ast

import ast
def noncify(username, nonce):
    notnonce=nonce.encode() if isinstance(nonce, str) else nonce
    return remotocrypt(username + notnonce)
def update(username, action="add"):
    file_path = "remotefuncs.py"
    
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: remotefuncs.py not found.")
        return

    with open(file_path, "w") as f:
        for line_num, line_content in enumerate(lines, 1):
            if line_num == 16 and "users =" in line_content:
                # Extract and parse the list
                parts = line_content.split("=")
                current_list_str = parts[1].strip()
                
                try:
                    current_list = ast.literal_eval(current_list_str)
                except Exception:
                    current_list = []
                
                # Logic for Add vs Remove
                if action == "add":
                    if username not in current_list:
                        current_list.append(remotocrypt(username))
                elif action == "remove":
                    if username in current_list:
                        current_list.remove(remotocrypt(username))

                # Write back the modified line
                f.write(f"    users = {current_list}\n")
            else:
                # Keep everything else exactly the same
                f.write(line_content)

def remotocrypt(x):
    return baseify(sha(x)).decode('utf-8')