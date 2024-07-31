import asyncio
import websockets
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import os
from datetime import datetime

image_directory = "./image"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

def is_valid_image(image_bytes):
    try:
        Image.open(BytesIO(image_bytes))
        # print("image OK")
        return True
    except UnidentifiedImageError:
        print("image invalid")
        return False

async def handle_connection(websocket, path):
    last_saved_time = datetime.now() 
    while True:
        try:
            message = await websocket.recv()
            # print(len(message))
            ip_address = websocket.remote_address[0]
            
            if len(message) > 5000:
                if is_valid_image(message):
                    current_time = datetime.now()
                    time_diff = (current_time - last_saved_time).total_seconds()

                    if time_diff >= 5: 
                        file_path = os.path.join(image_directory, f"{ip_address}.jpg")
                        
                        with open(file_path, "wb") as f:
                            f.write(message)
                        print(f"Saved image: {file_path}")

                        last_saved_time = current_time 

            print()
        except websockets.exceptions.ConnectionClosed:
            break

async def main():
    server = await websockets.serve(handle_connection, '0.0.0.0', 3001)
    await server.wait_closed()

asyncio.run(main())
