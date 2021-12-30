from os import listdir
import time
from PIL import Image
import base64
from io import BytesIO
from kmp import KMPSearch

def load_images(path):
    imglist = listdir(path)
    images = []
    for image in imglist:
        img = Image.open(path + image)
        images.append(img)
    return images

def encode_images(images):
    encoded_images = []
    for img in images:
        output = BytesIO()
        img.save(output,format = 'JPEG')
        img_data = output.getvalue()
        en = base64.b64encode(img_data)
        encoded_images.append(str(en))
        print("Length ",len(str(en)))
    return encoded_images

def concat(list):
    result = ''
    for item in list:
        result += item
    return result

path_dataset = "assets/dataset/"
path = "assets/input/"

if __name__ == '__main__':
    print("Loading and Encoding Dataset")
    cat_pics = load_images(path_dataset)
    cat_pics = encode_images(cat_pics)
    print("Done!")
    print("Loading and Encoding Input Data")
    input_image = load_images(path)
    input_image = encode_images(input_image)
    input_image = input_image[0]
    print("Done!")
    cat_pics = concat(cat_pics)
    #print("Cat Pics")
    #print(cat_pics)
    #print("Input Cat Pic")
    #print(input_image)
    t = time.time()
    KMPSearch(input_image,cat_pics)
    print("Time taken is ",time.time()-t)