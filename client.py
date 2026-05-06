#client.py
import websockets,asyncio
from remotefuncs import inpute, remotocrypt,noncify,getepass
async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("login") 
        nonce = await websocket.recv()
        username = inpute("Username: ")
        passwd = getepass()
        auth_token = noncify(username, nonce)
        await websocket.send(auth_token)
        response = await websocket.recv()
        print(response)
        
asyncio.run(main())