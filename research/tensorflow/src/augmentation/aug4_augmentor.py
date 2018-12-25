import numpy as np
from PIL import Image
from PIL import ImageFilter
import Augmentor


class GaussianNoise(Augmentor.Operation):

    def __init__(self, probability, radius):
        Augmentor.Operation.__init__(self, probability)
        self.radius = radius

    def perform_operation(self, images):
        def do(image):
            return image.filter(ImageFilter.GaussianBlur(radius=self.radius))

        augmented_images = []

        for image in images:
            augmented_images.append(do(image))

        return augmented_images


class EmbossNoise(Augmentor.Operation):

    def __init__(self, probability):
        Augmentor.Operation.__init__(self, probability)

    def perform_operation(self, images):
        def do(image):
            return image.filter(ImageFilter.EMBOSS)

        augmented_images = []

        for image in images:
            augmented_images.append(do(image))

        return augmented_images


class ContourNoise(Augmentor.Operation):

    def __init__(self, probability):
        Augmentor.Operation.__init__(self, probability)

    def perform_operation(self, images):
        def do(image):
            return image.filter(ImageFilter.CONTOUR)

        augmented_images = []

        for image in images:
            augmented_images.append(do(image))

        return augmented_images


# dataset_path = '../../images/dogscats500/training_data/cats'
# dataset_path = '/Users/lee/code/apteka/datasets/dataset02_rc/image1'
dataset_path = '/Users/lee/code/apteka/datasets/dataset03_pl/images-tantumverde'

p = Augmentor.Pipeline(
    source_directory=dataset_path,
    output_directory='augmentor'
)

# p.rotate(
#     probability=0.7,
#     max_left_rotation=10,
#     max_right_rotation=10
# )

# p.zoom(
#     probability=0.5,
#     min_factor=1.1,
#     max_factor=1.5
# )

# p.flip_left_right(
#     probability=0.8
# )
#
# p.flip_top_bottom(
#     probability=0.8
# )
#
# p.rotate_random_90(
#     probability=0.9
# )
#
# p.skew(
#     probability=0.9,
#     magnitude=0.5
# )
#
# p.crop_centre(
#     probability=0.5,
#     percentage_area=0.8,
#     randomise_percentage_area=False
# )

# noise = GaussianNoise(
#     probability=1.0,
#     radius=5
# )

noise = ContourNoise(
    probability=1.0
)

p.add_operation(noise)

p.sample(60)
