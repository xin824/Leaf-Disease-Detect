import os
'''
image_path = './test.JPG'
os.chdir('./model')
os.system('python3 ./leaf_seg_to_detect.py --image-path ../test.JPG')
os.chdir('../')'''

import subprocess

image_path = './test.JPG'
os.chdir('./model')
result = subprocess.run(['python3', './leaf_seg_to_detect.py','--image-path','../test.JPG',], capture_output=True, text=True)
#print(type(result))
if result.stdout:
    print('Pic not found.')
print(result.stdout)
os.chdir('../')



