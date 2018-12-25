import cv2
import numpy as np

# load color image
img = cv2.imread('../../images/napteka2.jpg')

# dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
# cv2.imwrite('output3b.jpg', dst)

# smooth the image with alternative closing and opening
# with an enlarging kernel
morph = img.copy()

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# take morphological gradient
gradient_image = cv2.morphologyEx(morph, cv2.MORPH_GRADIENT, kernel)

# split the gradient image into channels
image_channels = np.split(np.asarray(gradient_image), 3, axis=2)

channel_height, channel_width, _ = image_channels[0].shape

# apply Otsu threshold to each channel
for i in range(0, 3):
    _, image_channels[i] = cv2.threshold(~image_channels[i], 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    image_channels[i] = np.reshape(image_channels[i], newshape=(channel_height, channel_width, 1))

# merge the channels
image_channels = np.concatenate((image_channels[0], image_channels[1], image_channels[2]), axis=2)

gray = cv2.cvtColor(image_channels, cv2.COLOR_BGR2GRAY)
# gray = cv2.bilateralFilter(gray, 1, 10, 120)
# edges = cv2.Canny(gray, 10, 250)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
# morph = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
morph = cv2.erode(gray, kernel)

# save the denoised image
# cv2.imwrite('output3.jpg', morph)

cv2.imshow('Denoising', morph)
cv2.waitKey()
