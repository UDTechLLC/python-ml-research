import cv2


class WindowManager(object):
    def __init__(self, window_name, keypress_callback=None):
        self.keypressCallback = keypress_callback

        self._windowName = window_name
        self._isWindowCreated = False

    @property
    def is_window_created(self):
        return self._isWindowCreated

    def create_window(self):
        cv2.namedWindow(self._windowName + ' Original')
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True
        self.create_trackbar('diameter(for bilateralFilter)', 1, 30)
        self.create_trackbar('sigmaColor(for bilateralFilter)', 10, 255)
        self.create_trackbar('sigmaSpace(for bilateralFilter)', 120, 255)

        self.create_trackbar('threshold min(for Canny edge detection)', 10, 160)
        self.create_trackbar('threshold max(for Canny edge detection)', 250, 255)

        self.create_trackbar('kernel size(morphological structuring element)', 7, 20)

        self.create_trackbar('Contour area min amount points (*100)', 10, 300)

        self.create_trackbar('Approx edges amount', 4, 12)

    def show(self, original, output):
        cv2.imshow(self._windowName + ' Original', original)
        cv2.imshow(self._windowName, output)

    def destroy_window(self):
        cv2.destroyWindow(self._windowName + ' Original')
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def process_events(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)

    def create_trackbar(self, name, default_value, max_value):
        cv2.createTrackbar(name, self._windowName, default_value, max_value, self.on_change_trackbar)

    def get_trackbar_value(self, name):
        value = cv2.getTrackbarPos(name, self._windowName)
        return value

    @staticmethod
    def on_change_trackbar(event):
        pass
