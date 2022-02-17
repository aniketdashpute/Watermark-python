import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import glob2 as glob
import os
import sys
savedir = "./output/"

def AddWatermarkFolder(str_foldername, str_watermarkname, alpha1=1.0, alpha2=0.2):
    path = str_foldername + '/*.png*'

    for iter, path_name in enumerate(glob.glob(path)):
        print(path_name)
        AddWatermark(path_name, str_watermarkname, alpha1, alpha2)

def AddWatermark(str_imgname, str_watermarkname, alpha1=1.0, alpha2=0.2):
    # Load the image to be watermarked
    img = cv2.imread(str_imgname)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Load the watermark
    waterimg = cv2.imread(str_watermarkname)
    waterimg = cv2.cvtColor(waterimg, cv2.COLOR_BGR2RGB)
    
    waterimgRes = __MirrorResize(img, waterimg)
    
    # Blend both the images
    img_blend = cv2.addWeighted(img, alpha1, waterimgRes, alpha2, 0.0)
    
    img_blend_write = cv2.cvtColor(img_blend, cv2.COLOR_RGB2BGR)
    
    strsplit = str_imgname.split('/')
    str_out = savedir+strsplit[-1]
    #str_out = savedir+str_out
    cv2.imwrite(str_out, img_blend_write)
    
    return img_blend
    
    
def __MirrorResize(img, waterimg):
    # First make the watermark image the same size as source image
    waterimgRes = np.zeros(img.shape)

    # First, in height 0-dimension:
    if (img.shape[0] > waterimg.shape[0]):
        bottom_pad = img.shape[0] - waterimg.shape[0]
        waterimgRes = cv2.copyMakeBorder(waterimg, 0, bottom_pad, 0, 0, cv.BORDER_REPLICATE)
    else:
        waterimgRes = waterimg[:img.shape[0],:,:]

    # Now, in width 0-dimension:
    if (img.shape[1] > waterimgRes.shape[1]):
        right_pad = img.shape[1] - waterimgRes.shape[1]
        waterimgRes = cv2.copyMakeBorder(waterimgRes, 0, 0, 0, right_pad, cv.BORDER_REPLICATE)
    else:
        waterimgRes = waterimgRes[:,:img.shape[1],:]
        
    return waterimgRes


# Add main support to run file from terminal directly
if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])