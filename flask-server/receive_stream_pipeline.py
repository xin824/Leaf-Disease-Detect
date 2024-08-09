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
time_thre = 0.25
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
    delay = 1.5
    
    sst = float(((now - 60.0) if now >= (60.0 - delay ) else now) + delay)
    file_path = os.path.join(image_directory, ip_address, f"{str(('%.2f'%sst))}.jpg")
    image.save(file_path)
    print(f"Saved image: {file_path}")
    
    while(datetime.now().second - now > (delay - 0.5)):
        now = (now + time_thre) if (now + time_thre) < 60.0 else (now + time_thre - 60.0)
        sst = float(((now - 60.0) if now >= (60.0 - delay ) else now) + delay)
        file_path = os.path.join(image_directory, ip_address, f"{str(('%.2f'%sst))}.jpg")
        image.save(file_path)
        
        
        print(f"copy image: {file_path}")
        
    return now

async def handle_disconnect(ip_address):
    file_path_new = os.path.join(image_directory, ip_address, f"new.jpg")
    image = Image.open(file_path_new)
    image = image.resize((384, 288), Image.LANCZOS)
    
    path = os.path.join(image_directory, ip_address)
    await dir_check(path)
    for i in range(60 / time_thre):
        file_path = os.path.join(image_directory, ip_address, f"{str(('%.2f'%(float(i) * time_thre)))}.jpg")
        image.save(file_path)
        print(f"Saved image: {file_path}")
        
    path = os.path.join(image_directory2, ip_address)
    await dir_check(path)
    for i in range(60 / time_thre):
    
        file_path = os.path.join(image_directory2, ip_address, f"{str(('%.2f'%(float(i) * time_thre)))}.jpg")
        image.save(file_path)
        
    with app.app_context():
        control.set_plant_disconnect(ip_address)
        

    

async def handle_connection(websocket, path):
    last_saved_time = datetime.now()
    connected_clients = set()
    Clients.add(websocket)
    
    ''' read previously connected devices '''
    if not connected_clients:
        with open(device_id_directory, 'r', encoding = 'utf-8') as file:
        
            for line in file:
                line = line.strip()
                connected_clients.add(line)
    ip_address = websocket.remote_address[0]
    
    ''' add a column to the website and add a new image folder '''
    if(ip_address not in connected_clients):
        connected_clients.add(ip_address)
        with app.app_context():
            new_plant = control.add_plant(ip_address)
            add_device_ip(ip_address)
        print('add new device: ', ip_address)
        path = os.path.join(image_directory, ip_address)
        folder_path = os.path.dirname(path)
        os.makedir(folder_path)
        print('add new image folder: ', ip_address)
    
    ''' set this device's icon to connect '''
    with app.app_context():
        control.set_plant_connect(ip_address)
    print(ip_address, 'connect')
    
    folder_path = os.path.join(image_directory, ip_address)
    await dir_check(folder_path)
    
    now = datetime.now().second
    global message
    while True:
        try:
            message = await websocket.recv()
            
            ''' determine whether the message is a image '''
            if len(message) > 5000:
                if is_valid_image(message):
                
                    current_time = datetime.now()
                    time_diff = (current_time - last_saved_time).total_seconds()
                    ''' save a image every five seconds '''
                    if time_diff >= time_thre:                        
                        now = (now + time_thre) if (now + time_thre) < 60.0 else (now + time_thre - 60.0)
                        #st = float(((now+off) if (now+off)<60 else (now+off-60)))
                        
                        file_path_new = os.path.join(image_directory, ip_address, f"new.jpg")
                        save_path_new = os.path.join(image_directory, ip_address, f"annotation.jpg")
                        print("file path new: " + file_path_new)
                        print("save path new: " + save_path_new)
                        if os.path.exists(save_path_new):
                            os.remove(save_path_new)
                            print(f"File '{save_path_new}' has been deleted.")
                        else:
                            print(f"File '{save_path_new}' does not exist.")
                        
                        #with open(file_path_new, "wb") as f:
                        #    f.write(message)
                        
                        await write_image(file_path_new, message)
                        now = await save_image(file_path_new, ip_address, now)
                            
                        ''' run the model with the new image '''
                        #os.chdir('./model')
                        #result = subprocess.run(['python3', './module.py', '--image-path', '../'+file_path_new, '--save-path','../'+save_path_new], capture_output=True, text=True)
                        result = run_process('./model/yolo640leafdetect.mdla', './model/notbad_office_finetune.mdla', './model/det_seg_trans.mdla', file_path_new, 'import_test.jpg')
                        # print(result)
                        #os.chdir('../')
                        
                        if(os.path.exists(save_path_new)):
                            print("Found a saved image: " + save_path_new)
                            await save_image(save_path_new, ip_address)
                        '''
                        if result.stdout:
                        
                            state = read_model_result(result.stdout)
                            print(result.stdout)
                            print(f"Device: {ip_address} detect result: {state}")
                            if(state):
                                with app.app_context():
                                    updated_plant = control.update_plant_ip(ip_address, state, current_time.strftime('%Y/%m/%d %H:%M:%S'))
                        else:
                            print(f"pic not found: {file_path}")
                        '''
                        last_saved_time = current_time
        except websockets.exceptions.ConnectionClosed:
            ip_address = websocket.remote_address[0]
            await handle_disconnect(ip_address)
            print(ip_address, 'disconnect')
            break    
            
async def main():
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
        device_ip = read_device_ip()
        for ip in device_ip:
            handle_disconnect(ip)
            print(f"set device: {ip} disconnect")
        server.close()
        await server.wait_closed()
    
    


asyncio.run(main())
