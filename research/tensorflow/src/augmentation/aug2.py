import os
import re
import numpy as np
import cv2 as cv
import skimage as sk
from skimage import transform


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def get_classes(dir):
    classes = []
    for folder in sorted(os.scandir(dir), key=lambda e: e.name):
        # print(folder)
        if folder.is_dir():
            classes.append(os.path.split(folder.path)[-1])

    return classes


# preprocess_dataset
def preprocess_dataset():
    # (training) dataset directory
    training_dir = '../../images/dogscats500/training_data'

    # (training) dataset classes & subdirectories
    classes = get_classes(training_dir)
    print(classes)

    # for all images files
    for cls in classes:
        # do image preprocessing
        images_path = os.path.join(training_dir, cls)
        print(cls)
        for i, file in enumerate(sorted_aphanumeric(os.listdir(images_path)), start=1):
            if file == '.DS_Store':
                continue

            if i > 2:
                continue

            preprocess_image(cls, images_path, file)


noise_mode = ['none', 'gaussian', 'poisson', 'speckle']


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


def noise_func(image, intmode):
    if intmode == 0:
        pre = image
    else:
        # pre = sk.util.random_noise(image, mode=noise_mode[intmode])
        # pre = np.multiply(pre, 255.)
        pre = noisy(noise_mode[intmode], image)
    return pre


def flip_func(image, intpos):
    if intpos == 0:
        pre = image
    elif intpos == 1:
        pre = np.fliplr(image)
    elif intpos == 2:
        pre = np.flipud(image)
    else:
        pre = np.fliplr(image)
        pre = np.flipud(pre)
    return pre


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result


def rotate_func(image, intpos):
    if intpos == 0:
        pre = image
    else:
        # pre = sk.transform.rotate(image, angle=(90 * intpos))
        # pre = np.multiply(pre, 255.)
        pre = rotate_image(image, angle=(90 * intpos))
    return pre


# preprocess image
def preprocess_image(cls, images_path, image_file):
    preprocessed_dir = os.path.join('../../images/dogscats500/preprocessed', cls)

    image_filepath = os.path.join(images_path, image_file)
    print("    ", image_filepath)

    image = cv.imread(image_filepath)

    if not os.path.exists(preprocessed_dir):
        os.makedirs(preprocessed_dir)

    # flip * rotate * noise = 4 * 4 * 4
    # for noise_case in range(4):
    for flip_case in range(4):
        for rotate_case in range(4):
            preprocessed_image = rotate_func(flip_func(image, flip_case), rotate_case)
            # do save preprocessing image
            image_file_name, image_file_ext = os.path.splitext(image_file)[:2]
            preprocessed_name = image_file_name + '.' + str(flip_case) + str(rotate_case) + image_file_ext
            preprocessed_image_file = os.path.join(preprocessed_dir, preprocessed_name)
            print(preprocessed_image_file)
            cv.imwrite(preprocessed_image_file, preprocessed_image)
            # cv.imshow(preprocessed_name, preprocessed_image)


if __name__ == '__main__':
    preprocess_dataset()
