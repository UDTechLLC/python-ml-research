import numpy as np
import cv2
import threshold1

img = cv2.imread('../../../images/apteka1.jpg')

blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Remove noise


def edgedetect(channel):
    sobelX = cv2.Sobel(channel, cv2.CV_16S, 1, 0)
    sobelY = cv2.Sobel(channel, cv2.CV_16S, 0, 1)
    sobel = np.hypot(sobelX, sobelY)

    sobel[sobel > 255] = 255;  # Some values seem to go above 255. However RGB channels has to be within 0-255
    return sobel


def findSignificantContours(img, edgeImg):
    image, contours, heirarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(heirarchy[0])

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        # print(tupl)
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    # If contour isn't covering 5% of total area of image then it probably is too small
    tooSmall = edgeImg.size * 5 / 100
    for tupl in level1:
        contour = contours[tupl[0]]
        area = cv2.contourArea(contour)
        # print(contour, area, tooSmall)
        if area > tooSmall:
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
    # print ([x[1] for x in significant]);
    return [x[0] for x in significant]


edgeImg = np.max(np.array([edgedetect(blurred[:, :, 0]), edgedetect(blurred[:, :, 1]), edgedetect(blurred[:, :, 2])]),
                 axis=0)

mean = np.mean(edgeImg)
# Zero any value that is less than mean. This reduces a lot of noise.
edgeImg[edgeImg <= mean] = 0

edgeImg_8u = np.asarray(edgeImg, np.uint8)

'''
# Find contours
significant = findSignificantContours(img, edgeImg_8u)
print(significant)

# Mask
mask = edgeImg.copy()
mask[mask > 0] = 0
cv2.fillPoly(mask, significant, 255)
# Invert mask
mask = np.logical_not(mask)

# Finally remove the background
img[mask] = 0
'''

origin = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 120)
minLineLength = 20
maxLineGap = 5
lines = cv2.HoughLinesP(edgeImg_8u, 1, np.pi / 180, 100, minLineLength, maxLineGap)
# print(lines)

for line in lines:
    for x1, y1, x2, y2 in line:
        print(x1, x2, y1, y2)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 20)

threshold1.create_resized_window('origin', origin)
cv2.imshow('origin', origin)

threshold1.create_resized_window('edges', edges)
cv2.imshow('edges', edges)

threshold1.create_resized_window('lines', img)
cv2.imshow('lines', img)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
