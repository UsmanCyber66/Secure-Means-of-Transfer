import asyncio
import os
from remotefuncs import encrypt, sha, baseify, attr, serverlogin
import websockets
from websockets.exceptions import ConnectionClosed
async def handle_connection(websocket):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            if not attr.logged:
                result = await serverlogin(websocket, message)
                print(f"Auth Result: {result}")
            else:
                print(f"Current Directory: {os.listdir()}")
    except ConnectionClosed:
        print("Client disconnected.")

async def serveron():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket Server started on ws://localhost:8765")
        await asyncio.Future()  # This keeps the server running forever

if __name__ == "__main__":
    try:
        asyncio.run(serveron())
    except Exception as e:
        print(f"Server error: {e}")