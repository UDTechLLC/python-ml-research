import cv2


class ImageProcessor(object):
    def __init__(self, kernel):
        self._kernel = kernel

    def process(self, src, dst):
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 1, 10, 120)

        edges = cv2.Canny(gray, 10, 250)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, self._kernel)

        normalizedInverseAlpha = (1.0 / 255) * (255 - closed)
        channels = cv2.split(src)
        for channel in channels:
            channel[:] = channel * normalizedInverseAlpha
        cv2.merge(channels, dst)
        print(dst.ctypes)


class SimpleImageProcessor(ImageProcessor):
    def __init__(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        ImageProcessor.__init__(self, kernel)
