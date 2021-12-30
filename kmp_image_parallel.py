from os import listdir
import multiprocessing
import time
from PIL import Image
import base64
from io import BytesIO

def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)
 
    # create lps[] that will hold the longest prefix suffix 
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]
 
    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
 
    i = 0 # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1
 
        if j == M:
            print("Found pattern at index " + str(i-j))
            j = lps[j-1]
 
        # mismatch after j matches
        elif(i < N and pat[j] != txt[i]):
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
                
def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix
 
    lps[0] # lps[0] is always 0
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i]== pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar 
            # to search step.
            if len != 0:
                len = lps[len-1]
 
                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1

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

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    numprocs = multiprocessing.cpu_count()

    t = time.time()
    KMPSearch(input_image,cat_pics)
    print("Time taken is ",time.time()-t)