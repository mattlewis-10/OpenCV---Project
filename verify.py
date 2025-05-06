# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:51:27 2025

@author: ludwi
"""

import cv2
import numpy as np
from image_utils import (
   preprocess_for_sift,
   convert_to_binary,
   resize_watermark,
   extract_lsb_pattern
)

def verify_watermark(image, watermark, n_keypoints=100, match_threshold=0.7):
    """
    Verify if the watermark is present in the image.

    Args:
        image (np.ndarray): The image to check.
        watermark_img (np.ndarray): The original watermark image.
        n_keypoints (int): Number of keypoints to check.
        match_threshold (float): Percentage of matches required to confirm presence.

    Returns:
        bool: True if watermark is detected, False otherwise.
        float: Match percentage.
    
    """
    
    gray = preprocess_for_sift(image)
    
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:n_keypoints]
    
    h, w = image.shape[:2]
    binary_watermark = convert_to_binary(watermark)
    if binary_watermark.shape != (3, 3):
      binary_watermark = resize_watermark(binary_watermark, (3, 3))
      
    matches = 0
    
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        extracted_pattern = extract_lsb_pattern(image, (x, y))
        
        #Compare patterns
        if np.array_equal(extracted_pattern, binary_watermark):
            matches += 1
    
    match_percentage = matches / len(keypoints) if keypoints else 0
    
    is_present = match_percentage >= match_threshold
    
    return is_present, match_percentage
            
    
            
            
    
    
    
    
    
    