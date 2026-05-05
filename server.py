import asyncio
import os
from remotefuncs import encrypt, sha, baseify, attr, serverlogin
import websockets
from websockets.exceptions import ConnectionClosed
global num
num=0
async def serveron():
    async def handle_connection(websocket):
        global num
        num=0
        try:
            async for message in websocket:
                num= num+ 1
                if num==1:
                    serverlogin(message)
                else:
                    print(os.listdir()) #just for testing. 
        except ConnectionClosed:
            print("Client disconnected gracefully.")
        except Exception as e:
            print(f"Error: {e}")

    async def main():
        # Start the server on localhost, port 8765
        async with websockets.serve(handle_connection, "localhost", 8765):
            print("WebSocket Server started on ws://localhost:8765")
            await asyncio.Future()  # This keeps the server running forever

    await main()

if __name__ == "__main__":
    asyncio.run(serveron())