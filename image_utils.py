# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:52:47 2025

@author: ludwi
"""

import cv2
import numpy as np
from scipy.ndimage import rotate

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


def rotate_watermark_pattern(pattern, angle):
    rotated = rotate(pattern, angle, reshape=False, order=0, mode='nearest')
    return (rotated > 0.5).astype(np.uint8)

def scale_watermark_pattern(pattern, target_size):
    return cv2.resize(pattern, (target_size, target_size), interpolation=cv2.INTER_NEAREST)


def select_watermark_pattern(x, y, w, h, binary_watermark, angle):
    
    #Return an adapted watermark pattern based on keypoint position and angle
    
    if x < w / 2 and y < h / 2:
        # Top-left: rotate pattern
        adapted_wm = rotate_watermark_pattern(binary_watermark, angle)
    elif x >= w / 2 and y < h / 2:
        # Top-right: flip vertically
        adapted_wm = np.flipud(binary_watermark)
    elif x < w / 2 and y >= h / 2:
        # Bottom-left: flip horizontally
        adapted_wm = np.fliplr(binary_watermark)
    else:
        # Bottom-right: rotate + flip horizontally
        rotated = rotate_watermark_pattern(binary_watermark, angle)
        adapted_wm = np.fliplr(rotated)

    return adapted_wm

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

def extract_lsb_pattern(image, center, size=3):
    """
    Extract the LSB pattern from a region centered at a keypoint.

    """
    cx, cy = center
    h, w = image.shape[:2]
    half = size // 2
    pattern = np.zeros((size, size), dtype=np.uint8)

    for dy in range(-half, half + 1):
        for dx in range(-half, half + 1):
            x, y = cx + dx, cy + dy
            if 0 <= x < w and 0 <= y < h:
                # Extract LSB from red channel (index 2)
                pattern[dy + half, dx + half] = image[y, x, 2] & 1
            else:
                # If out of bounds, default to 0
                pattern[dy + half, dx + half] = 0

    return pattern

# -----------------------------
# EMBEDDED IMAGE TAMPERING
# -----------------------------

def crop_image(image, fraction=0.4):
    
    #Crop Top-Left Portion of Image
    h, w = image.shape[:2]
    x_start = int(w * fraction)
    y_start = int(h * fraction)
    
    return image[y_start:, x_start:]

def rotate_image(image, angle=30):
    
    #Rotate image around centre at certain angle
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    
    return cv2.warpAffine(image, matrix, (w, h))

def resize_image(image, scale=0.5):
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

def compress_image(image, output_path="temp_compressed.jpg", quality=30):
    cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    return cv2.imread(output_path)




