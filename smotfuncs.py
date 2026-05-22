import hashlib,os, json,base64,getpass,asyncio, websockets,random,ast
from cryptography.fernet import Fernet

def sha(x):
    if isinstance(x, str):
        return hashlib.sha256(x.encode()).digest()
    else:
        return hashlib.sha256(x).digest()
def shasafe(x):
    return hashlib.sha256(x.encode()).hexdigest()
def baseify(x):
    return base64.urlsafe_b64encode(x)
class attr:
    password: str| bytes= "default"
    username:  str | bytes = "default"
    messages = {"ls":"os.listdir()", "pwd":"os.getcwd()", "cat":"open(args).read()"}
    logged=False
    users = ['DdZUmJ1szx6wg8rYC6txxFkAJRM0vs5Km8lXi4Sexjs=']
    @classmethod
    def get_key(cls):
        
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
        if value:  
            return value
        print("Input cannot be empty. Please try again.")
        
def getepass(prompt="Enter Password: "):
    while True:
        pw = getpass.getpass(prompt)
        if pw.strip():  
            return pw
        print("Password cannot be empty!")
        

async def serverlogin(websocket, message): 
    try:    
        
        nonce = str(random.randint(100000, 999999)) 
        await websocket.send(nonce) 
        
        
        cr = await websocket.recv()
        cr= cr.strip().replace("|", " ").split()
        
        for i in attr.users:
            if noncify(i, nonce) == cr[0]:
                with open(i,'r') as f:
                    data=json.load(f)
                if noncify(data["combohash"], nonce)== cr[1]:
                    attr.logged = True
                await websocket.send("Login successful!")
                print("Client authenticated successfully.")
                break
        else:
            await websocket.send("Login failed!")
    except Exception as e:
        print(f"Login error: {e}")
        return "Error"


def noncify(username, nonce):
    notnonce=nonce.encode() if isinstance(nonce, str) else nonce
    username_bytes = username.encode() if isinstance(username, str) else username
    return remotocrypt(username_bytes + notnonce)
import ast

import ast

def update(object,list,action):
    if action!="add" or "remove":
        print("Please enter a valid action")
    if action=="add":
        with open('users.json', 'r') as file:
            data = json.load(file)
        data[list].append(remotocrypt(object))
    if action=="remove":
        try:
            with open("users.json","r")as file:
                data= json.load(file)
            data[list].remove(list.index(object))
        except Exception:
            print(Exception)    
def remotocrypt(x):
    return baseify(sha(x)).decode('utf-8')
async def forever(websocket, message):
    if message in attr.messages:
        
        result = eval(attr.messages[message])
        
        await websocket.send(str(result))
