from .transforma_bound import Bound
from .transforma_seg import Segment
from .transforma_detect import Detect
from NeuronRuntimeHelper import NeuronContext
from PIL import Image
import argparse
import numpy as np
import cv2
import time
import os

def detect_process(detect, img_resized, initial):
    # detect = Detect(mdla_path=mdla_path_detect)

    # Initialize model
    if initial:
        ret = detect.Initialize()
        if ret != True:
            print("Failed to initialize model")
            return

    
    output_array = []
    class_names = ['blight', 'citrus' ,'healthy', 'measles', 'mildew', 'mite', 'mold', 'rot', 'rust', 'scab', 'scorch', 'spot', 'virus']
    
    
    for bound_img in img_resized:
        input_array = detect.img_preprocess(bound_img)

        detect.SetInputBuffer(input_array, 0)
        
        # Execute model
        ret = detect.Execute()
        if ret != True:
            print("Failed to Execute")
            return

        output_array.append(class_names[np.argmax(detect.GetOutputBuffer(0))])
        
        disease = class_names[np.argmax(detect.GetOutputBuffer(0))]
    
    final_disease = "No leaf"
    if len(output_array) > 0:
        final_disease = "healthy"
    print(output_array)
    for i in output_array:
        if(i != "healthy"):
            final_disease = i
    
    
    return output_array, final_disease
