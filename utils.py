from PIL import Image
import numpy as np

def load_image(imagePath):
    image = Image.open(imagePath)
    img_data = np.array(list(image.getdata()), np.uint8)

    width, height = image.size
    return img_data, width, height