from NeuronRuntimeHelper import NeuronContext
from PIL import Image
import argparse
import numpy as np
import cv2
import time

class Segment(NeuronContext):

    def __init__(self, mdla_path: str = "None"):
        super().__init__(mdla_path)


    def img_preprocess(self, image):

        # Convert to NumPy array with the correct dtype
        dtype = np.float32
        dst_img = np.array(image, dtype=dtype)
        dst_img = dst_img / 255.0
    
        # 如果模型要求输入是四维的，例如 U-Net 等模型通常要求输入是 (batch_size, height, width, channels)
        dst_img = np.expand_dims(dst_img, axis=0)  # 扩展维度添加 batch_size 维度

        return dst_img
    
    def create_mask(self, pred_mask):
        pred_mask = np.argmax(pred_mask, axis=-1)
        pred_mask = pred_mask[..., np.newaxis]
        return pred_mask

    def postprocess(self, image):

        bgr_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        return bgr_img

def main(mdla_path, image_path):

    start_time = time.time()
    model = Segment(mdla_path=mdla_path)

    # Initialize model
    ret = model.Initialize()
    if ret != True:
        print("Failed to initialize model")
        return

    # Load input image
    image = Image.open(image_path)
    image = image.resize((128, 128))

    input_array = model.img_preprocess(image)

    model.SetInputBuffer(input_array, 0)

    # Execute model
    ret = model.Execute()
    if ret != True:
        print("Failed to Execute")
        return

    image = model.GetOutputBuffer(0)
    need = model.create_mask(image)
    
    white_images = np.zeros_like(input_array[0])
    wants = np.array([np.where(need == 0, input_array[0], white_images)])
    
    model.postprocess(wants[0])




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Detect model with NeuronHelper')
    parser.add_argument('--dla-path', type=str, default='seg_diff_layer.mdla',
                        help='Path to the Detection mdla file')
    parser.add_argument('--image-path', type=str, default='rust_test.jpg',
                        help='Path to the input image')
    args = parser.parse_args()

    main(args.dla_path, args.image_path)
