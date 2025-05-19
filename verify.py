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
    
    gray = preprocess_for_sift(image)
    
    #Detect Keypoints
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:n_keypoints]
    
    #Prepare Watermark
    binary_watermark = convert_to_binary(watermark)
    if binary_watermark.shape != (3, 3):
      binary_watermark = resize_watermark(binary_watermark, (3, 3))
      
    matches = 0
    mismatched_kps = [] #Array of mismatched keypoints
    
    #Extract Watermark
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        extracted_pattern = extract_lsb_pattern(image, (x, y))
        
        #Compare patterns
        if extracted_pattern is not None and extracted_pattern.shape == binary_watermark.shape:
            if np.array_equal(extracted_pattern, binary_watermark):
                matches += 1
            else:
                mismatched_kps.append(kp)
                
        else:
            mismatched_kps.append(kp)
    
    match_percentage = matches / len(keypoints) if keypoints else 0
    
    is_present = match_percentage >= match_threshold
    
    return is_present, match_percentage, mismatched_kps
            
    
            
            
    
    
    
    
    
    