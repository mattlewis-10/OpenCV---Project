# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:51:00 2025

@author: ludwi
"""

import cv2
from image_utils import preprocess_for_sift, convert_to_binary, resize_watermark, apply_lsb_pattern

def embed_watermark(cover_img, watermark_img, n_keypoints=100):
    
    #Step 1: Preprocess
    gray = preprocess_for_sift(cover_img)
    
    #Step 2: Detect SIFT keypoints
    sift = cv2.SIFT_create()
    keypoints = sift.detect(gray, None)
    keypoints = sorted(keypoints, key=lambda x: -x.response)[:n_keypoints] #Pick strongest keypoints
    
    if len(keypoints) < 1:
        raise ValueError("Not enough keypoints detected for watermarking")
    
    #Step 3: Prepare watermark
    binary_watermark = convert_to_binary(watermark_img)
    
    if binary_watermark.shape != (3, 3):
        binary_watermark = resize_watermark(binary_watermark, (3, 3))
        
    #Step 4: Embed watermark
    embedded_img = cover_img.copy()
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        embedded_img = apply_lsb_pattern(embedded_img, (x, y), binary_watermark)
        
    return embedded_img
    