import numpy as np
import cv2

img = cv2.imread('../../images/apteka4.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'''
img = cv2.GaussianBlur(img, (3, 3), 0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

scale = 1
delta = 0
ddepth = cv2.CV_16S
grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
# Gradient-Y
# grad_y = cv.Scharr(gray,ddepth,0,1)
grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)

abs_grad_x = cv2.convertScaleAbs(grad_x)
abs_grad_y = cv2.convertScaleAbs(grad_y)

res = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
'''

# res = cv2.adaptiveThreshold(img, maxValue=255,
#                               adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
#                               thresholdType=cv2.THRESH_BINARY, blockSize=11, C=2)

res = cv2.Canny(gray, 230, 150)

im2, contours, h = cv2.findContours(res, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
        area = cv2.contourArea(cnt)
        if area > 10:
            print("square")
            print(cnt)
            print(area)
            cv2.drawContours(res, [cnt], 0, (255, 0, 0), -1)

cv2.imshow('img', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
