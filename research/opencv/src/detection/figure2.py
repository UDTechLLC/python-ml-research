import cv2
import numpy


def enhancing_contrast(img):
    # equalize the histogram of the input image
    histeq = cv2.equalizeHist(img)
    return histeq


def stroke_edges(src, dst, blurKsize=7, edgeKsize=5):
    if blurKsize >= 3:
        blurredSrc = cv2.medianBlur(src, blurKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize=edgeKsize)
    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha
    cv2.merge(channels, dst)


def detection_edge(img):
    # It is used depth of cv2.CV_64F.
    sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)

    # Kernel size can be: 1,3,5 or 7.
    sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    canny = cv2.Canny(img, 50, 240)

    stroke = stroke_edges(img)
    return stroke


if __name__ == '__main__':
    image = cv2.imread('output2.jpg')
    # new_image = detection_edge(image)
    new_image = image.copy()
    stroke_edges(image, new_image, 7, 9)

    cv2.imshow('Original', image)
    cv2.imshow('Processed', new_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()