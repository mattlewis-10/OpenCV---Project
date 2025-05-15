# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 16:52:06 2025

@author: ludwi
"""

from verify import verify_watermark

def get_tampering_cause(percentage, threshold):
    # (upper bound, cause description)
    rules = [
        (0.0, "No watermark detected — severe tampering"),
        (0.2, "Very low match — likely heavy cropping or format conversion"),
        (0.5, "Partial match — possible resizing or partial crop"),
        (threshold, "Minor mismatch"),
        (1.0, "Watermark intact — no tampering detected")
    ]

    for upper_bound, cause in rules:
        if percentage <= upper_bound:
            return cause

def detect_tampering(image, watermark, n_keypoints=100, threshold=0.7):
    
    #Watermark Verification
    is_present, match_pct = verify_watermark(image, watermark, n_keypoints=n_keypoints, match_threshold=threshold)
    
    tampered = not is_present
    
    cause = get_tampering_cause(match_pct, threshold)
    
    return tampered, match_pct, cause