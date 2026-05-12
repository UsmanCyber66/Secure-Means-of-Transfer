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
    users = ['Nt5SeyrdEyxqwuzdtbGiM6DsDAwceLwa6JYQK8qhB3Q=']
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
        cr = cr.strip().replace("|"," ").split()
        if len(cr) ==2:
            for i in attr.users:
                if noncify(i, nonce) == cr[0]:
                    with open(cr[1], 'r') as f:
                        data=json.load(f)
                    if cr[1]==data["combohash"]:
                        attr.logged = True
                        websocket.send("Login Completed!")
                        print("Client Authenticated Successfully!")
            else:
                await websocket.send("Login failed!")
        else:
            await websocket.send("Invalid Format\n Login Failed!")
    except Exception as e:
        print(f"Login error: {e}")
        return "Error"


def noncify(username, nonce):
    notnonce=nonce.encode() if isinstance(nonce, str) else nonce
    username_bytes = username.encode() if isinstance(username, str) else username
    return remotocrypt(username_bytes + notnonce)
def update(username, action="add"):
    file_path = "smotfuncs.py"
    
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: smotfuncs.py not found.")
        return

    with open(file_path, "w") as f:
        for line_num, line_content in enumerate(lines, 1):
            if line_num == 16 and "users =" in line_content:
                
                parts = line_content.split("=")
                current_list_str = parts[1].strip()
                
                try:
                    current_list = ast.literal_eval(current_list_str)
                except Exception:
                    current_list = []
                
                
                if action == "add":
                    if username not in current_list:
                        current_list.append(remotocrypt(username))
                elif action == "remove":
                    if username in current_list:
                        current_list.remove(remotocrypt(username))

                
                f.write(f"    users = {current_list}\n")
            else:
                
                f.write(line_content)

def remotocrypt(x):
    return baseify(sha(x)).decode('utf-8')
async def forever(websocket, message):
    if message in attr.messages:
        
        result = eval(attr.messages[message])
        
        await websocket.send(str(result))