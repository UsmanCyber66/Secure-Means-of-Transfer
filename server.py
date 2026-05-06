import asyncio
import os
import websockets
from websockets.exceptions import ConnectionClosed
# Importing your custom utilities from remotefuncs
from remotefuncs import encrypt, sha, baseify, attr, serverlogin

async def handle_connection(websocket):
    print("Client connected.")
    try:
        # The main message loop for the connection
        async for message in websocket:
            print(f"Received: {message}")
            
            # Use the global attribute to check auth status
            if attr.logged== False:
                # We pass the websocket object so serverlogin can send the nonce
                result = await serverlogin(websocket, message)
                print(f"Auth Result: {result}")
            else:
                # Once authenticated, provide functional results
                print(f"Auth active. Current Directory: {os.listdir()}")
                # You can add logic here to send the listdir back to the client
                await websocket.send(str(os.listdir()))
                
    except ConnectionClosed:
        print("Client disconnected gracefully.")
    except Exception as e:
        print(f"Error in connection handler: {e}")

async def serveron():
    # Setting up the server on your HP laptop's localhost
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket Server started on ws://localhost:8765")
        # Keeps the server alive indefinitely
        await asyncio.Future()  

if __name__ == "__main__":
    try:
        # Start the main event loop
        asyncio.run(serveron())
    except Exception as e:
        print(f"Server execution error: {e}")