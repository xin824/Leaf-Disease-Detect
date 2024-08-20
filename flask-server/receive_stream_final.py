import asyncio
import websockets
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import os
import sys
from datetime import datetime
from model import *
import control
import math
from config import app
import subprocess
import signal


Clients= set()
device_id_directory = 'device_ip.txt'
image_directory = "../plant/build/image"
image_directory2 = "../plant/public/image"
fps = 6
initial = True
bound = Bound(mdla_path='./model/yolo640leafdetect_v2.mdla')
segment = Segment(mdla_path='./model/for_yolo_seg_v2.mdla')
detect = Detect(mdla_path='./model/best_model_seg_aug_v5.mdla')
connected_clients = set()

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
    lines_array = lines.splitlines()
    print(lines_array)
    for line in lines_array:
        if(line in class_names):
            return line
    return 'No leaf'

def add_device_ip(new_ip):
    with open(device_id_directory, 'a', encoding = 'utf-8') as file:
        file.write(new_ip + '\n')

def is_valid_image(image_bytes):
    try:
        Image.open(BytesIO(image_bytes))
        return True
    except UnidentifiedImageError:
        print("image invalid")
        return False

async def broadcast():
    while True:
        for ws in Clients:
            await ws.send("ping")
        await asyncio.sleep(5)

async def dir_check(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print('add new folder: ', path)

async def write_image(file_path_new, m):
    with open(file_path_new, "wb") as f:
        f.write(m)

async def save_image(file_path_new, ip_address, now):
    image = Image.open(file_path_new)
    image = image.resize((384, 288), Image.LANCZOS)
    file_path = ""
    #off = time_thre if (now.microsecond / 1000000 > time_thre) else 0
    delay = 2.0
    
    # sst = float(((now - 60.0) if now >= (60.0 - delay ) else now) + delay)
    sst = int((now + delay) % (fps))
    # file_path = os.path.join(image_directory, ip_address, f"{str(('%.2f'%sst))}.jpg")
    file_path = os.path.join(image_directory, ip_address, f"{str(sst)}.jpg")
    image.save(file_path)
    print(f"Saved image: {file_path}")
    print(f"================================: {now}")
    
    return now

async def handle_disconnect(ip_address):
    new = os.path.join(image_directory, ip_address, f"new.jpg")
    ann = os.path.join(image_directory, ip_address, f"annotation.jpg")
    new_copy = os.path.join(image_directory2, ip_address, f"new.jpg")
    ann_copy = os.path.join(image_directory2, ip_address, f"annotation.jpg")
    with app.app_context():
        control.set_plant_disconnect(ip_address)
    image = Image.open(new)
    image.save(new_copy)
    image = Image.open(ann)
    image.save(ann_copy)
        
async def create_plant(ip_address):
    connected_clients.append(ip_address)
    print(connected_clients)
    with app.app_context():
        new_plant = control.add_plant(ip_address)
        add_device_ip(ip_address)
    print('add new device: ', ip_address)
    folder_path = os.path.join(image_directory, ip_address)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    print('add new image folder: ', folder_path)
        
async def handle_connection(websocket, path):
    ip_address = websocket.remote_address[0]
    
    ''' add a column to the website and add a new image folder '''
    if(ip_address not in connected_clients):
        await create_plant(ip_address)
    
    ''' set this device's icon to connect '''
    with app.app_context():
        control.set_plant_connect(ip_address)
    print(ip_address, 'connect')
    
    global message, initial, bound, segment, detect
    file_path_new = os.path.join(image_directory, ip_address, f"new.jpg")
    save_path_new = os.path.join(image_directory, ip_address, f"annotation.jpg")
                    
    while True:
        try:
            message = await websocket.recv()
            
            ''' determine whether the message is a image '''
            if len(message) > 5000:
                
                if is_valid_image(message):
                    current_time = datetime.now()
                    await write_image(file_path_new, message)      
                    percent, result = run_process(bound, segment, detect, file_path_new, save_path_new, initial)
                    if initial:
                        initial = False
                    
                    if result != "":
                        with app.app_context():
                            updated_plant = control.update_plant_ip(ip_address, percent + result, current_time.strftime('%Y/%m/%d %H:%M:%S'))
                    else:
                        print(f"pic not found: {file_path_new}")
                    
        except websockets.exceptions.ConnectionClosed:
            ip_address = websocket.remote_address[0]
            await handle_disconnect(ip_address)
            print(ip_address, 'disconnect')
            break    
            
async def main():
    global connected_clients
    connected_clients = read_device_ip()
    server = await websockets.serve(handle_connection, '0.0.0.0', 3001)
    
    stop_event = asyncio.Event()
    
    def handle_signal():
        stop_event.set()
    
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_signal)
    loop.add_signal_handler(signal.SIGTERM, handle_signal)
    
    try:
        await stop_event.wait()
    finally:
        ''' set device disconnect when websocket close'''
        for ip in connected_clients:
            handle_disconnect(ip)
            print(f"set device: {ip} disconnect")
        server.close()
        await server.wait_closed()

asyncio.run(main())
