# -*- coding: utf-8 -*-
"""
Created on Fri May  2 14:39:00 2025

@author: ludwi
"""

import numpy as np
import cv2

watermark = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
    ], dtype=np.uint8) * 255 #Scale for image

#Save as image file
cv2.imwrite('assets/watermark.png', watermark)
print("Saved watermark.png")