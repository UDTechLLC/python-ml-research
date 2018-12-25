import numpy as np
import skimage as sk
from skimage import transform
import cv2 as cv
# import tensorflow as tf


def noisy(noise_typ, image):
    if noise_typ == "gaussian":
        row, col, ch = image.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy = image + gauss
        return noisy

    elif noise_typ == "s&p":
        row, col, ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0
        return out

    elif noise_typ == "poisson":
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy

    elif noise_typ == "speckle":
        row, col, ch = image.shape
        gauss = np.random.randn(row, col, ch)
        gauss = gauss.reshape(row, col, ch)
        noisy = image + image * gauss
        return noisy


def augment_image(image):
    # popular augmentation techniques

    # flip
    flip_1 = np.fliplr(image)
    # cv.imshow('flip_1', flip_1)
    flip_2 = np.flipud(image)
    # cv.imshow('flip_2', flip_2)
    flip_3 = np.flipud(flip_1)
    # cv.imshow('flip_3', flip_3)

    # rotation
    rotate_1 = sk.transform.rotate(image, 90)
    rotate_2 = sk.transform.rotate(image, 180)
    rotate_3 = sk.transform.rotate(image, 270)
    # cv.imshow('rotate_1', rotate_1)
    # cv.imshow('rotate_2', rotate_2)
    # cv.imshow('rotate_3', rotate_3)

    # scale
    # scale_1 = sk.transform.rescale(image, scale=2.0, mode='constant')
    # scale_2 = sk.transform.rescale(image, scale=0.5, mode='constant')
    # cv.imshow('scale_1', scale_1)
    # cv.imshow('scale_2', scale_2)

    # noise
    # noise_value = 0
    # noise_0 = np.multiply(image, 1 / 255)
    # noise_1 = noise_0
    # noise_1[:, :, 2] = noise_1[:, :, 2] + noise_value
    # noise_1 = np.multiply(noise_1, 255.0)
    # noise_2 = noise_0
    # noise_2[:, :, 1] = noise_2[:, :, 1] + noise_value
    # noise_2 = np.multiply(noise_2, 255.0)
    # noise_3 = noise_0
    # noise_3[:, :, 0] = noise_3[:, :, 0] + noise_value
    # noise_3 = np.multiply(noise_3, 255.0)
    # cv.imshow('noise_0', noise_0)
    # cv.imshow('noise_1', noise_1)
    # cv.imshow('noise_2', noise_2)
    # cv.imshow('noise_3', noise_3)

    # random noise
    # rnoise_1 = sk.util.random_noise(image, mode='gaussian')
    # rnoise_2 = sk.util.random_noise(image, mode='poisson')
    # rnoise_3 = sk.util.random_noise(image, mode='speckle')
    # cv.imshow('rnoise_1', rnoise_1)
    # cv.imshow('rnoise_2', rnoise_2)
    # cv.imshow('rnoise_3', rnoise_3)

    xnoise_1 = noisy("speckle", image)
    cv.imshow('xnoise_1', xnoise_1)


img_path = '../../images/dogscats500/training_data'
img_filename = img_path + '/cats/cat.0.jpg'
img = cv.imread(img_filename)
cv.imshow('img', img)
augment_image(img)

cv.waitKey()
