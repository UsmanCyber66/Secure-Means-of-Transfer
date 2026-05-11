import asyncio
import os
import websockets
from websockets.exceptions import ConnectionClosed
from smotfuncs import encrypt, sha, baseify, attr, serverlogin, forever

async def handle_connection(websocket):
    print("Client connected.")
    try:
        async for message in websocket:
            if attr.logged==False:
                await serverlogin(websocket,message)
            else:
                await forever(websocket,message)
    except ConnectionClosed:
        print("Client disconnected gracefully.")
        attr.logged = False
    except Exception as e:
        print(f"Error in connection handler: {e}")
        attr.logged = False

async def serveron():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket Server started on ws://localhost:8765")
        await asyncio.Future()  

if __name__ == "__main__":
    try:
        asyncio.run(serveron())
    except Exception as e:
        print(f"Server execution error: {e}")