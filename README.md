<p align="center">
  <picture>
    <img src="./assets/LOGO_ROUNDED.png" alt="SMoT Logo" width="500" style="max-width: 100%; border-radius: 20px;">
  </picture>
</p>

# Secure Means of Transfer 
is a tool that is built  _**FULLY IN Python**_, and is a lighter, faster alternative to SCP(Secure CoPy) , and can run even on a small microcontroller(coming 
soon).SMoTuses a simple fernet encryption and does NOT require a full operating system , rather it requires only python. SMot is used to send or recieve files through a server, much like of SCP, but also can execute commands, handles data, users, and passwords efficiently, all data is sent through a lightweight WebSocket. The data being sent is encrypted using a Fernet key, which is derived from the password of the user by first hashing it with sha256 then wrapping it in base64. The Login authentication is done using a Nonce(Number used once) . This tool is built on the assumption that someone is **Always watching** . **NOTE: Tool is Still under development**

### ***THIS SOFTWARE IS LICENSED UNDER THE GNU GENERAL PUBLIC LICENSE v3***
#ProudlyPython
