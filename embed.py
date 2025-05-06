# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:51:00 2025

@author: ludwi
"""

import cv2
from image_utils import(
    preprocess_for_sift, 
    convert_to_binary, 
    resize_watermark,
    select_watermark_pattern,
    scale_watermark_pattern,
    apply_lsb_pattern    
)

def embed_watermark(image, watermark, n_keypoints=100):
    
    #Step 1: Preprocess
    gray = preprocess_for_sift(image)
    
    #Step 2: Detect SIFT keypoints
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:n_keypoints] #Pick strongest keypoints
    
    if len(keypoints) < 1:
        raise ValueError("Not enough keypoints detected for watermarking")
    
    #Step 3: Prepare watermark
    binary_watermark = convert_to_binary(watermark)
    if binary_watermark.shape != (3, 3):
        binary_watermark = resize_watermark(binary_watermark, (3, 3))
        
    #Step 4: Embed watermark
    h, w = image.shape[:2]
    embedded_img = image.copy()
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        angle = kp.angle
        size = max(int(kp.size / 5), 3) #Keep minimum 3x3
        
        
        adapted_wm = select_watermark_pattern(x, y, w, h, binary_watermark, angle)
        size = size if size % 2 == 1 else size + 1
        scaled_wm = scale_watermark_pattern(adapted_wm, size)
        
        embedded_img = apply_lsb_pattern(embedded_img, (x, y), scaled_wm)
        
    return embedded_img
    