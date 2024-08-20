from .transforma_bound import Bound
from .transforma_seg import Segment
from .transforma_detect import Detect
from NeuronRuntimeHelper import NeuronContext
from multiprocessing import Pool, cpu_count
from PIL import Image
import argparse
import uuid
import numpy as np
import cv2
import time
import os

def create_mask(pred_mask):
    pred_mask = np.argmax(pred_mask, axis=-1)
    pred_mask = pred_mask[..., np.newaxis]
    return pred_mask


def segment_process(segment, img_resized, initial):
    # segment = Segment(mdla_path=mdla_path_segment)

    # Initialize model
    
    if initial:
        ret = segment.Initialize()
        if ret != True:
            print("Failed to initialize model")
            return

    img_segmented = []
    masks = []

    for bound_img in img_resized:

        input_array = segment.img_preprocess(bound_img)

        segment.SetInputBuffer(input_array, 0)

        # Execute model
        ret = segment.Execute()
        if ret != True:
            print("Failed to Execute")
            return
            
        image = segment.GetOutputBuffer(0)

        need = segment.create_mask(image)

        white_images = np.zeros_like(input_array[0])

        wants = np.array([np.where(need == 0, input_array[0], white_images)])
        masks.append(need)
        img_segmented.append(wants[0] * 255)
    
    return img_segmented, masks


    
