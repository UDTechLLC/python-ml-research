import os
from PIL import Image

DATASETS_DIR = '/Users/lee/code/apteka/datasets/'


def get_classes(dir):
    classes = []
    for folder in sorted(os.scandir(dir), key=lambda e: e.name):
        # print(folder)
        if folder.is_dir():
            classes.append(os.path.split(folder.path)[-1])
    return classes


def rescale_image(file, scale):
    img = Image.open(file)
    size = (img.size[0], img.size[1])
    side = max(size[0], size[1])
    base = int(side * scale)

    if side == img.size[0]:
        percent = (base / float(img.size[0]))
        calc = int((float(img.size[1]) * float(percent)))
        size = (base, calc)
    else:
        percent = (base / float(img.size[1]))
        calc = int((float(img.size[0]) * float(percent)))
        size = (calc, base)

    return img.resize(size, Image.ANTIALIAS)


def rescale_dataset(source_dataset, output_dataset, scale):
    classes = get_classes(source_dataset)
    print(classes)

    if not os.path.exists(output_dataset):
        os.makedirs(output_dataset)

    for cls in classes:
        print(cls)
        source_images_path = os.path.join(source_dataset, cls)
        output_images_path = os.path.join(output_dataset, cls)

        if not os.path.exists(output_images_path):
            os.makedirs(output_images_path)

        for file in os.listdir(source_images_path):
            if file == '.DS_Store':
                continue

            print(file)

            rescaled_image = rescale_image(os.path.join(source_images_path, file), scale)
            rescaled_image.save(os.path.join(output_images_path, file), quality=95)


if __name__ == '__main__':
    # rescale_dataset(
    #     source_dataset=os.path.join(DATASETS_DIR, 'dataset02_rc1'),
    #     output_dataset=os.path.join(DATASETS_DIR, 'dataset02_rc'),
    #     scale=0.2
    # )

    rescale_dataset(
        source_dataset=os.path.join(DATASETS_DIR, 'dataset03_pl0'),
        output_dataset=os.path.join(DATASETS_DIR, 'dataset03_pl'),
        scale=0.4
    )
