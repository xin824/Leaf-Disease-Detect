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

def run_process(mdla_path_bound, mdla_path_segment, mdla_path_detect, image_path, save_path):
    return main(mdla_path_bound, mdla_path_segment, mdla_path_detect, image_path, save_path)

def main(mdla_path_bound, mdla_path_segment, mdla_path_detect, image_path, save_path):
    
    image = Image.open(image_path)
    
    start_time = time.time()
    print("Start Bound time: 0ms")
    
    img_resized, bound_output, original_image = bound_process(mdla_path_bound, image)
    
    
    bound_total = time.time()
    # print("Finish Bound time: " + str(bound_total - start_time) + "ms")

    '''Segmentation'''
    
    segment_time = time.time()
    # print("Start Segment time: " + str(segment_time - start_time) + "ms")
    
    # Wait unitl segmentation model done.
    img_segmented = segment_process(mdla_path_segment, img_resized)
    
    end_segment_time = time.time()
    # print("End Segment time: " + str(end_segment_time - start_time) + "ms")

    '''Detect Leaf Disease'''
    detect_start = time.time()
    # print("Start detect time: " + str(detect_start - start_time) + "ms")
    
    output_array, final_disease = detect_process(mdla_path_detect, img_segmented)
    
    detect_total = time.time()
    # print("Finish Detect time: " + str(detect_total - start_time) + "ms")
    
    # print("Detection spended time: " + str(detect_total - detect_start) + "ms")
    
    end_time = time.time()
    total_time = end_time - start_time
    # print("Total time: " + str(total_time) + 'ms')

    
    fancy_time = time.time()
    # print("Before adding fancy mask: " + str(fancy_time - start_time) + "ms")

    # annotation_process(save_path, output_array, bound_output, original_image)
    
    fancy_time_end = time.time()
    print("Finish adding fancy mask: " + str(fancy_time_end - start_time) + "ms")
    return final_disease



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Detect model with NeuronHelper')
    parser.add_argument('--dla-bound-path', type=str, default='yolo640leafdetect.mdla',
                        help='Path to the Bound mdla file')
    parser.add_argument('--dla-segment-path', type=str, default='for_yolo_seg.mdla',
                        help='Path to the Segmentation mdla file')
    parser.add_argument('--dla-detect-path', type=str, default='det_seg_trans.mdla',
                        help='Path to the Detection mdla file')
    parser.add_argument('--image-path', type=str, default='bound_test.JPG',
                        help='Path to the input image')
    parser.add_argument('--save-path', type=str, default='../../plant/build/image/',
                        help='Path to save the image')

    args = parser.parse_args()
    main(args.dla_bound_path, args.dla_segment_path, args.dla_detect_path, args.image_path, args.save_path)
