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
import asyncio
from multiprocessing import Pool, cpu_count

def return_prediction_for_image(output_array, bound_boxes, img_resized, masks, original_image):
    blended = []
    try:
        for result, img_res, mask in zip(output_array, img_resized, masks):
            overlay_color = np.array([0, 0, 255])
            if(result == "healthy"):
                overlay_color = np.array([0, 255, 0])

            overlay = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
            overlay[:, :, 0] = overlay_color[0] 
            overlay[:, :, 1] = overlay_color[1]
            overlay[:, :, 2] = overlay_color[2]

            img_res = np.array(img_res)    
            non_zero_mask = np.broadcast_to(mask != 1, img_res.shape)
            other_mask = np.broadcast_to(mask == 1, img_res.shape)
            overlay[other_mask] = 255

            alpha = 0.2
            
            blend = cv2.addWeighted(img_res, 1 - alpha, overlay, alpha, 0)
            blended.append(blend)
    except:
        print("Overlay fail")
    try:
        test = original_image.copy()
        for blend, bound_box in zip(blended, bound_boxes):
            x = bound_box[0]
            y = bound_box[1]
            w = bound_box[2]
            h = bound_box[3]
            side = max(w, h)
            sub_img = cv2.resize(blend, (side, side))
            # cv2.imshow("resize anno", sub_img)
            # cv2.waitKey(2000)
            
            if(w > h):
                start_y = int((w - h) / 2)      
                sub_img = sub_img[start_y:start_y + h,:]
            else:
                start_x = int((h - w) / 2)
                sub_img = sub_img[:, start_x:start_x + w]
            

            test[y:y+h, x:x+w] = sub_img
            
        return test

    except:
        print("Push back fail")


def draw_boxes(image, box, score, class_id, color=(0, 255, 0)):

        # Convert the box coordinates to integers
        x1, y1, w, h = [int(v) for v in box]
        
        # Set the color for the bounding box
        # Draw the bounding box on the image
        cv2.rectangle(image, (x1, y1), (x1 + w, y1 + h), color, 2)
        
        # Define the label text
        label = f"{class_id}: {score:.2f}"  # class_id: confidence
        
        # Calculate the size of the label text
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        
        # Determine the position of the label on the image
        label_x = x1
        label_y = y1
        
        # Add a rectangular background to the label
        cv2.rectangle(
            image,
            (int(label_x), int(label_y)),
            (int(label_x), int(label_y)),
            color,
            cv2.FILLED,
        )


def draw_bbox_on_image(output_image, output_array, bound_output):
        img_w = 128 * 3
        img_h = 128 * 3
        output = bound_output
        # Initilize lists to store bounding box coordinates, scores and class_ids
        outputs = cv2.transpose(output[0])
        
        # Initilize lists to store bounding box coordinates, scores and class_ids

    
        boxes = []
        scores = []
        class_ids = []


        # outputs = np.array([cv2.transpose(output_buf[0])])
        rows = outputs.shape[0]
        for i in range(rows):
            classes_scores = outputs[i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    int((outputs[i][0] - (0.5 * outputs[i][2])) * img_w),
                    (outputs[i][1] - (0.5 * outputs[i][3])) * img_h,
                    outputs[i][2] * img_w,
                    outputs[i][3] * img_h,
                ]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        # Filter out low confidence bounding boxes using non-maximum suppression
        indices = cv2.dnn.NMSBoxes(
            boxes, scores, 0.5, 0.5
        )
        
        if len(indices) == 0:
            print("No indices candidate.")
            return None
        cur = 0
        
        for i in indices:
            x, y, w, h = boxes[i] 
            x = (int(x) if int(x) > 0 else 0)
            y = (int(y) if int(y) > 0 else 0)
            w = (int(w) if int(w) > 0 else 0)
            h = (int(h) if int(h) > 0 else 0)
            
            if(w * h > (img_h * img_w / 49)):
                disease = output_array[cur]
                cur = cur + 1
                color = (0, 0, 255)
                if(disease == "healthy"):
                    color = (0, 255, 0)
                draw_boxes(output_image, boxes[i], scores[i], class_ids[i], color)
        return output_image
   

# def annotation_process(save_path, output_array, bound_output, original_image, img_resized, masks, bound_boxes):
def annotation_process(save_path, output_array, bound_output, original_image, img_resized, bound_boxes):
        
    try:
        # segment_img_with_overlay = overlay_mask_on_image(need, original_image, color)

        original_image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        # overlay_image = return_prediction_for_image(output_array, bound_boxes, img_resized, masks, original_image)

        original_image = cv2.resize(original_image, (128*3, 128*3))

        annotated_image = draw_bbox_on_image(original_image, output_array, bound_output)

        
        
    except:
        print("No image")
    
    
    
    try:
        annotated_image = annotated_image[48:336, 0:384]
        
    except:
        annotated_image = cv2.resize(original_image, (128*3, 128*3))
        annotated_image = annotated_image[48:336, 0:384]
        print("Annotation failed")
    
    cv2.imwrite(save_path, annotated_image, [cv2.IMWRITE_JPEG_QUALITY, 60])
    
    
    print("image:" + save_path)

    
    
