# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:52:47 2025

@author: ludwi
"""

import cv2
import numpy as np

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
    
# -----------------------------
# PRE-PROCESSING
# -----------------------------

def preprocess_for_sift(image):
    #Ensure the image is grayscale for SIFT
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

# -----------------------------
# WATERMARK HANDLING
# -----------------------------

def convert_to_binary(image):
    #Convert an image to binary
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    _, binary = cv2.threshold(gray, 127, 1, cv2.THRESH_BINARY)
    
    return binary

def resize_watermark(watermark, size):
    resized = cv2.resize(watermark, size, interpolation=cv2.INTER_NEAREST)
    return resized

def select_watermark_pattern(x, y, width, height):
    #Return a binary 3x3 pattern based on keypoint location
    if x < width and y < height / 2:
        #Top-Left: X pattern
        return np.array([1, 0, 1], [0, 1, 0], [1, 0, 1])
    elif x >= width and y < height / 2:
        #Top-Right: + pattern
        return np.array([0, 1, 0], [1, 1, 1], [0, 1, 0])
    elif x < width / 2 and y >= height / 2:
        #Bottom-Left: block pattern
        return np.array([1, 1, 1], [1, 0, 1], [1, 1, 1])
    else:
        #Bottom-Right: \ pattern
        return np.array([1, 0, 0], [0, 1, 0], [0, 0, 1])

# -----------------------------
# LSB STEGANOGRAPHY
# -----------------------------

def set_lsb(value, bit):
    return (value & ~1) | bit

def apply_lsb_pattern(image, center, pattern):
    """
    Apply a binary 3x3 pattern to the LSBs of the pixel values
    centered around the given (x, y) keypoint.
    
    """
    img = image.copy()  # Don't modify the original
    cx, cy = center     # Keypoint coordinates (x, y)
    h, w = img.shape[:2]
    half = pattern.shape[0] // 2  # Half of 3 = 1

    for dy in range(-half, half + 1):  # From -1 to +1
        for dx in range(-half, half + 1):
            x, y = cx + dx, cy + dy    # New pixel location
            if 0 <= x < w and 0 <= y < h:
                for c in range(3):  # For each color channel (B, G, R)
                    original = img[y, x, c]          # Get pixel value
                    bit = pattern[dy + half, dx + half]  # Get corresponding watermark bit
                    img[y, x, c] = set_lsb(original, bit) # Set new LSB
    return img




