**Remote** is a tool that is built in Pure _**Python**_, and is a lighter, faster alternative to SCP(Secure CoPy) , and can run even on a small microcontroller(coming 
soon).This tool uses a simple fernet encryption and does NOT require a full operating system , rather it requires only python. Remote handles data, users, and 
passwords efficiently, all data is sent through a lightweight WebSocket. The data being sent is encrypted using a Fernet key, which is derived from the password of the 
user by first hashing it with sha256 then wrapping it in base64. The Login authentication is done using a Nonce(Number used once) . This tool is built on the assumption that someone is **Always watching**

**                                                                THIS TOOL IS LICENSED UNDER GPLv3 **
#ProudlyPython
