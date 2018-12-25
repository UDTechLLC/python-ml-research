import cv2
import numpy as np

img = cv2.imread('../../images/output1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
# dst = cv2.cornerHarris(gray, 4, 5, 0.04)  # to detect only sharp corners
dst = cv2.cornerHarris(gray, 14, 5, 0.04) # to detect soft corners

# Result is dilated for marking the corners
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst > 0.01 * dst.max()] = [0, 0, 0]

cv2.imshow('Harris Corners', img)
cv2.waitKey()
