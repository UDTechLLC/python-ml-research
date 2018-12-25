import cv2
import configparser


class WindowManager(object):
    def __init__(self, window_name, keypress_callback=None):
        self.keypressCallback = keypress_callback

        self._originalWindowName = window_name + ' Original'
        self._processesWindowName = window_name + ' Processed'
        self._roiWindowName = 'ROI'
        self._isWindowCreated = False

    @property
    def is_window_created(self):
        return self._isWindowCreated

    def create_window(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        cv2.namedWindow(self._originalWindowName, cv2.WINDOW_NORMAL)

        cv2.namedWindow(self._processesWindowName, cv2.WINDOW_NORMAL)
        self.create_trackbar(
            'Diameter (bilateralFilter)',
            int(config['MAIN_CAMERA']['DIAMETER_BILATERAL_FILTER']),
            int(config['MAX_LIMIT']['DIAMETER_BILATERAL_FILTER_MAX'])
        )
        self.create_trackbar(
            'SigmaColor (bilateralFilter)',
            int(config['MAIN_CAMERA']['SIGMA_COLOR_BILATERAL_FILTER']),
            int(config['MAX_LIMIT']['SIGMA_BILATERAL_FILTER_MAX'])
        )
        self.create_trackbar(
            'SigmaSpace (bilateralFilter)',
            int(config['MAIN_CAMERA']['SIGMA_SPACE_BILATERAL_FILTER']),
            int(config['MAX_LIMIT']['SIGMA_BILATERAL_FILTER_MAX'])
        )

        self.create_trackbar(
            'Threshold min (Canny edge detection)',
            int(config['MAIN_CAMERA']['THRESHOLD_CANNY_MIN']),
            int(config['MAX_LIMIT']['THRESHOLD_CANNY_MIN_MAX'])
        )
        self.create_trackbar(
            'Threshold max (Canny edge detection)',
            int(config['MAIN_CAMERA']['THRESHOLD_CANNY_MAX']),
            int(config['MAX_LIMIT']['THRESHOLD_CANNY_MAX_MAX'])
        )

        self.create_trackbar(
            'Kernel size (morphological operation)',
            int(config['MAIN_CAMERA']['KERNEL_SIZE_MORPHOLOGICAL']),
            int(config['MAX_LIMIT']['KERNEL_SIZE_MORPHOLOGICAL_MAX'])
        )

        self.create_trackbar(
            'Contour area min amount points (*1000)',
            int(config['MAIN_CAMERA']['COUNTOUR_AREA_MIN_POINTS']),
            int(config['MAX_LIMIT']['COUNTOUR_AREA_MIN_POINTS_MAX'])
        )

        # self.create_trackbar('Approx edges amount', 4, 12)

        cv2.namedWindow(self._roiWindowName, cv2.WINDOW_NORMAL)

        cv2.resizeWindow(
            self._originalWindowName,
            int(config['WINDOWS_SIZE']['WINDOW_WIDTH']),
            int(config['WINDOWS_SIZE']['WINDOW_HEIGHT'])
        )
        cv2.moveWindow(self._originalWindowName, 0, 0)

        cv2.resizeWindow(
            self._processesWindowName,
            int(config['WINDOWS_SIZE']['WINDOW_WIDTH']),
            int(config['WINDOWS_SIZE']['WINDOW_WIDTH'])
        )
        cv2.moveWindow(
            self._processesWindowName,
            int(config['WINDOWS_SIZE']['WINDOW_WIDTH']),
            0
        )

        cv2.resizeWindow(
            self._roiWindowName,
            int(config['WINDOWS_SIZE']['WINDOW_ROI_SIZE']),
            int(config['WINDOWS_SIZE']['WINDOW_ROI_SIZE'])
        )
        cv2.moveWindow(
            self._roiWindowName,
            0,
            int(config['WINDOWS_SIZE']['WINDOW_HEIGHT'])
        )

        self._isWindowCreated = True

    def show(self, original, output, roi):
        if original is not None:
            cv2.imshow(self._originalWindowName, original)
        if output is not None:
            cv2.imshow(self._processesWindowName, output)
        if roi is not None:
            cv2.imshow(self._roiWindowName, roi)

    def destroy_window(self):
        cv2.destroyWindow(self._originalWindowName)
        cv2.destroyWindow(self._processesWindowName)
        cv2.destroyWindow(self._roiWindowName)
        self._isWindowCreated = False

    def process_events(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK.
            keycode &= 0xFF
            self.keypressCallback(keycode)

    def create_trackbar(self, name, default_value, max_value):
        cv2.createTrackbar(name, self._processesWindowName, default_value, max_value, self.on_change_trackbar)

    def get_trackbar_value(self, name):
        value = cv2.getTrackbarPos(name, self._processesWindowName)
        return value

    @staticmethod
    def on_change_trackbar(event):
        pass
