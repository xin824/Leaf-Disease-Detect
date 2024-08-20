from .transforma_bound import Bound
from .transforma_seg import Segment
from .transforma_detect import Detect
from .bound_process import *
from .segment_process import *
from .detect_process import *
from .annotation_process import *
from NeuronRuntimeHelper import NeuronContext
from PIL import Image
import argparse
import numpy as np
import cv2
import time
import os

def initial_model(model):
    ret = model.Initialize()
    if ret != True:
        print("Failed to initialize model")
        return None
    else:
        return model
        
def run_process(bound, segment, detect, image_path, save_path, initial):
    
    return main(bound, segment, detect, image_path, save_path, initial)

def main(bound, segment, detect, image_path, save_path, initial):
    
    image = Image.open(image_path)

    
    start_time = time.time()
    print("Start Bound time: 0ms")
    
    img_resized, bound_output, original_image, bound_imgs, bound_boxes = bound_process(bound, image, initial)
    
    if len(img_resized) == 0:
        print("No image bounded")
        
    bound_total = time.time()
    print("Finish Bound time: " + str(bound_total - start_time))


    '''Segmentation'''
    
    segment_time = time.time()
    print("Start segment: " + str(time.time() - start_time))
    
    # Wait unitl segmentation model done.
    img_segmented, masks = segment_process(segment, img_resized, initial)
    
    end_segment_time = time.time()
    print("Finish segment: " + str(time.time() - start_time))

    '''Detect Leaf Disease'''
    detect_start = time.time()
    print("Start detect: " + str(time.time() - start_time))
    
    output_array, final_disease = detect_process(detect, img_segmented, initial)
    
    print(output_array)
    if(len(output_array)):
        percentage = str(int(round(output_array.count('healthy') / len(output_array), 2) * 100)).zfill(3)
    else:
        percentage = '000'


    # annotation_process(save_path, output_array, bound_output, original_image, img_segmented, masks, bound_boxes)
    annotation_process(save_path, output_array, bound_output, original_image, img_resized, bound_boxes)
    
    fancy_time_end = time.time()
    print("Finish adding fancy mask: " + str(fancy_time_end - start_time) + "ms")
    return percentage, final_disease



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Detect model with NeuronHelper')
    parser.add_argument('--dla-bound-path', type=str, default='yolo640leafdetect.mdla',
                        help='Path to the Bound mdla file')
    parser.add_argument('--dla-segment-path', type=str, default='for_yolo_seg_v2.mdla',
                        help='Path to the Segmentation mdla file')
    parser.add_argument('--dla-detect-path', type=str, default='best_model_seg_aug_v3.mdla',
                        help='Path to the Detection mdla file')
    parser.add_argument('--image-path', type=str, default='bound_test.JPG',
                        help='Path to the input image')
    parser.add_argument('--save-path', type=str, default='../../plant/build/image/',
                        help='Path to save the image')

    args = parser.parse_args()
    main(args.dla_bound_path, args.dla_segment_path, args.dla_detect_path, args.image_path, args.save_path)
