import os
from PIL import Image, UnidentifiedImageError
image_directory = "../plant/build/image"
ip_address = "172.20.10.5"
save_path_new = os.path.join(image_directory, ip_address, f"final.jpg")
image = Image.open(save_path_new)
for i in range(60):
    file_path = os.path.join(image_directory, ip_address, f"{str(i)}.jpg")
    image.save(file_path)
    print(f"Saved image: {file_path}")
