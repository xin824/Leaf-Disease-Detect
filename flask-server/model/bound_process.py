from .transforma_bound import Bound
from .transforma_seg import Segment
from .transforma_detect import Detect
from NeuronRuntimeHelper import NeuronContext
from PIL import Image
import argparse
import uuid
import numpy as np
import math
import cv2
import time
import os

def bound_process(bound, image, initial):
    
    start = time.time()
    
    if image.mode == 'RGBA':
        # 转换为 RGB，去除alpha通道
        image = image.convert('RGB')
    
    img_w, img_h = image.size
    offset = abs(img_w - img_h)
    
    back = Image.new("RGB", (img_w, img_w), "black")
    offset = ((img_w - img_w) // 2, (img_w - img_h) // 2)
    back.paste(image, offset)
    
    img = cv2.cvtColor(np.array(back), cv2.COLOR_RGB2BGR)
    back_img = back.copy()
    
    # PIL: RGB, cv2: BGR
    # Preprocess input image
    # bound = Bound(mdla_path=mdla_path_bound)
    
    if initial:
        # Initialize model
        ret = bound.Initialize()
        if ret != True:
            print("Failed to initialize model")
            return
            
    input_array = bound.img_preprocess(back_img)
    # Set input buffer for inference
    bound.SetInputBuffer(input_array, 0)
    ret = bound.Execute()
    if ret != True:
        print("Failed to Execute")
        return
        
    bound_output = bound.GetOutputBuffer(0)
    bound_boxes = []
    bound_imgs = []
    try:
        bound_imgs, bound_boxes = bound.postprocess(back_img)
    except:
        print("No bounded object")
        
    img_resized = []

    
    try:
        for bound_img in bound_imgs:
            try:
                bound_img_resized = cv2.resize(bound_img, (128, 128), interpolation=cv2.INTER_LANCZOS4)
                img_resized.append(bound_img_resized)
            except:
                print("No leaf")    
    except:
        print("No pic yet.")
    
    return img_resized, bound_output, back_img, bound_imgs, bound_boxes
  
