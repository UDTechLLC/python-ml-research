import os
import re
import numpy as np
import cv2 as cv
import albumentations as A


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def get_classes(dir):
    classes = []
    for folder in sorted(os.scandir(dir), key=lambda e: e.name):
        if folder.is_dir():
            classes.append(os.path.split(folder.path)[-1])

    return classes


def preprocess_dataset():
    training_dir = '../../images/dogscats500/training_data'

    classes = get_classes(training_dir)
    print(classes)

    # for all images files
    for cls in classes:
        images_path = os.path.join(training_dir, cls)
        print(cls)
        for i, file in enumerate(sorted_aphanumeric(os.listdir(images_path)), start=1):
            if os.path.isdir(os.path.join(images_path, file)):
                continue

            if file == '.DS_Store':
                continue

            if i > 10:
                continue

            preprocess_image(cls, images_path, file)


# preprocess image
def preprocess_image(cls, images_path, image_file):
    preprocessed_dir = os.path.join('../../images/dogscats500/preprocessed', cls)

    image_filepath = os.path.join(images_path, image_file)
    print("    ", image_filepath)

    image = cv.imread(image_filepath)

    if not os.path.exists(preprocessed_dir):
        os.makedirs(preprocessed_dir)

    aug = A.Compose(
        transforms=[
        A.RandomRotate90(),
        A.Flip()],
        p=0.5)

    image_file_name, image_file_ext = os.path.splitext(image_file)[:2]
    print(image_file_name, image_file_ext)
    preprocessed_name = image_file_name + '.aug' + image_file_ext
    preprocessed_image_file = os.path.join(preprocessed_dir, preprocessed_name)
    print(preprocessed_name)
    print(preprocessed_image_file)

    preprocessed_image = aug(image=image)['image']

    cv.imwrite(preprocessed_image_file, preprocessed_image)


if __name__ == '__main__':
    preprocess_dataset()