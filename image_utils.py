# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:52:47 2025

@author: ludwi
"""

import cv2
import numpy as np
from PIL import Image

# -----------------------------
# IMAGE I/O
# -----------------------------

def load_image(path, grayscale=False):
    #Loads an image in either greyscale or color
    flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    image = cv2.imread(path, flag)
    
    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")
        
    return image

def save_image(image, path):
    #Saves image to file
    cv2.imwrite(path, image)