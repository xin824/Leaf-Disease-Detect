import os
'''
image_path = './test.JPG'
os.chdir('./model')
os.system('python3 ./leaf_seg_to_detect.py --image-path ../test.JPG')
os.chdir('../')'''

import subprocess

def read_model_result(lines):
    class_names = ['blight','citrus' ,'healthy', 'measles', 'mildew', 'mite', 'mold', 'rot', 'rust', 'scab', 'scorch', 'spot', 'virus']
    lines_array = lines.splitlines()
    for line in lines_array:
        if(line in class_names):
            return line
    return None

image_path = './test.JPG'
os.chdir('./model')
#result = subprocess.run(['python3', './leaf_seg_to_detect.py','--image-path','../../plant/build/image/172.20.10.5.jpg',], capture_output=True, text=True)
result = subprocess.run(['python3', './module.py','--image-path','../005.jpg',], capture_output=True, text=True)
print(result.stdout)
#print(read_model_result(result.stdout))
os.chdir('../')



