import asyncio
import websockets
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import os
from datetime import datetime
import control
from config import app
import subprocess

Clients = set()
device_id_directory = 'device_ip.txt'
image_directory = "../plant/build/image"
image_directory2 = "../plant/src/public/image"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
    
def read_device_ip():
    lines = []
    with open(device_id_directory, 'r', encoding = 'utf-8') as file:
        for line in file:
            line = line.strip()
            lines.append(line)
    return lines

def read_model_result(lines):
    class_names = ['blight','citrus' ,'healthy', 'measles', 'mildew', 'mite', 'mold', 'rot', 'rust', 'scab', 'scorch', 'spot', 'virus']
    for line in lines:
        line = line.strip()
        if(line in class_names):
            return line
    return None

def add_device_ip(new_ip):
    with open(device_id_directory, 'a', encoding = 'utf-8') as file:
        file.write(new_ip + '\n')

def is_valid_image(image_bytes):
    try:
        Image.open(BytesIO(image_bytes))
        # print("image OK")
        return True
    except UnidentifiedImageError:
        print("image invalid")
        return False

async def broadcast():
    while True:
        for ws in Clients:
            await ws.send("ping")
        await asyncio.sleep(5)

async def handle_connection(websocket, path):
    last_saved_time = datetime.now()
    connected_clients = set()
    if not connected_clients:
        with open(device_id_directory, 'r', encoding = 'utf-8') as file:
            for line in file:
                line = line.strip()
                connected_clients.add(line)
    while True:
        try:
            message = await websocket.recv()
            
            Clients.add(websocket)
            ip_address = websocket.remote_address[0]
            
            with app.app_context():
                control.set_plant_connect(ip_address)
                
            if(ip_address not in connected_clients):
                connected_clients.add(ip_address)
                with app.app_context():
                    new_plant = control.add_plant(ip_address)
                    add_device_ip(ip_address)
            
            with app.app_context():
                control.set_plant_connect(ip_address)
            #if(message == "pong"):
            #    print('recieve pong from ip:', ip_address)
            #    with app.app_context():
            #        control.set_plant_connect(ip_address)
            if len(message) > 5000:
                if is_valid_image(message):
                    current_time = datetime.now()
                    time_diff = (current_time - last_saved_time).total_seconds()
                    update_time = current_time.stdout.split(".", 1)

                    if time_diff >= 5: 
                        file_path = os.path.join(image_directory, f"{ip_address}.jpg")
                        
                        with open(file_path, "wb") as f:
                            f.write(message)
                        
                        file_path2 = os.path.join(image_directory2, f"{ip_address}.jpg")
                        
                        with open(file_path2, "wb") as f:
                            f.write(message)
                        print(f"Saved image: {file_path}")
                        
                        os.chdir('./model')
                        result = subprocess.run(['python3', './leaf_seg_to_detect.py','--image-path','../test.JPG',], capture_output=True, text=True)
                        os.chdir('../')
                        
                        if result.stdout:
                            state = read_model_result(result.stdout)
                            print(state)
                            if(state):
                                with app.app_context():
                                    updated_plant = control.update_plant_ip(ip_address, result.stdout, update_time[0])
                        
                        last_saved_time = current_time
                            
        except websockets.exceptions.ConnectionClosed:
            ip_address = websocket.remote_address[0]
            print(ip_address, 'disconnect')
            with app.app_context():
                control.set_plant_disconnect(ip_address)
            break
            
async def main():    
    server = await websockets.serve(handle_connection, '0.0.0.0', 3001)
    #await asyncio.gather(
    #    websockets.serve(handle_connection, '0.0.0.0', 3001, ping_interval=None),
    #    broadcast()
    #)
    await server.wait_closed()


asyncio.run(main())
