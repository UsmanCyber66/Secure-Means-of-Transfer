#client.py
import websockets,asyncio
from smotfuncs import baseify, inpute, remotocrypt,noncify,getepass, sha
async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("login")
        nonce=await websocket.recv()
        print("Nonce:",nonce)
        username = inpute("Username: ")
        passwd=getepass("Password:")
        usertoken=noncify(baseify(sha(username)), nonce)
        combohash= noncify(baseify(sha(username))+remotocrypt(passwd), nonce) 
        auth_token = str(usertoken)+ "|" + str(combohash)
        await websocket.send(auth_token)
        response = await websocket.recv()
        print(response)
        while True:
            await websocket.send(input())
            print(await websocket.recv())
asyncio.run(main())