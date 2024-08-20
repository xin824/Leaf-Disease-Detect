import os
from model import *
'''
image_path = './test.JPG'
os.chdir('./model')
os.system('python3 ./leaf_seg_to_detect.py --image-path ../test.JPG')
os.chdir('../')'''

import subprocess
from model import *

def read_model_result(lines):
    class_names = ['blight','citrus' ,'healthy', 'measles', 'mildew', 'mite', 'mold', 'rot', 'rust', 'scab', 'scorch', 'spot', 'virus']
    lines_array = lines.splitlines()
    for line in lines_array:
        if(line in class_names):
            return line
    return None

image_path = './test.JPG'
os.chdir('./model')
fine_tune_dir = "./healthy"

#result = subprocess.run(['python3', './leaf_seg_to_detect.py','--image-path','../../plant/build/image/172.20.10.5.jpg',], capture_output=True, text=True)
# for i in os.listdir(fine_tune_dir):
#    result = run_process('./yolo640leafdetect.mdla', './for_yolo_seg_v2.mdla', './det_nonseg_trans_aug_v2.mdla', os.path.join(fine_tune_dir, i), '../tt_test.jpg')
# result = subprocess.run(['python3', './module.py','--image-path','../002.jpg',], capture_output=True, text=True)
# print(result)
#print(read_model_result(result.stdout))

bound = Bound(mdla_path='./yolo640leafdetect_v2.mdla')
segment = Segment(mdla_path='./for_yolo_seg_v2.mdla')
detect = Detect(mdla_path='./best_model_seg_aug_v3.mdla')

percentage = run_process(bound, segment, detect, '../005.jpg', '../bestmodel_test.jpg', True)
print(percentage[0] + " " + percentage[1])
os.chdir('../')


