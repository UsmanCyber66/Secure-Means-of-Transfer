<p align="center">
  <picture>
    <img src="./assets/LOGO_ROUNDED.png" alt="SMoT Logo" width="500" style="max-width: 100%; border-radius: 20px;"> 
  </picture>
  
</p>

# Secure Means of Transfer
Secure Means of Transfer, or SMoT is a small Python tool that is built for fast and secure file transfers. SMoT uses SHA256 to hash and store passwords. Logins are authenticated through a custom nonce challenge similar to HMAC. 
## The Nonce challenge : 
### Step 1 : Send the Nonce and check the username
The Server sends a nonce, The client sends back an authentication token + command to execute which should be `hashed-and-nonced-username|hashed-andnonced-combohash|command-to-execute` . The combohash is `base64(sha256(username+password)). The server then checks the authentication token splits the authentication token from the '|' symbol, encrypts the first part before the first '|' with the nonce,checks it against a list of hashed usernames, if a user is found, then the server goes to Step2
### Step 2: Check Combohash
The Username now checked, the server now opens a JSON file that is named `base64(sha256(username)) that contains the combohash, the server encrypts the present combohash with the nonce and compares it to the token which is after the first '|' symbol , if it matches, we move to Step3
### Step 3 : Execute command
The user now fully recognized, the server now checks the command placed after the second '|' symbol against its list of allowed commands. If it is allowed, then the server executes it using ` eval(command) ` and returns the output to the client.   
**NOTE: Tool is Still under development**
## Why SMoT?
 - It's written in Python.
 Can run on all your devices, microcontrollers included. 
 - It's Lightweight!
 SMoT uses the Websockets and Asyncio libraries in Python for fast and asynchronous transfers
 - It's small.
 It is only a few MegaBytes (MB) .
## Try it out!
Clone it using 
```bash
git clone https://github.com/UsmanCyber66/Secure-Means-of-Transfer
```

### *This Software is licensed Under The GNU General Public License v3*
#ProudlyPython
