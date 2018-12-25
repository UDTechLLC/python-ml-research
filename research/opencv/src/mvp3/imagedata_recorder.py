import cv2
import processing
from capture_manager import CaptureManager
from threading import Thread


class ImageDataRecorder(object):
    def __init__(self, window_manager):
        self._record_face = 0
        self._record_count = 0
        self._stopped = True
        self._processed = False

        self._amount_frames = 0
        self._success_finding_contours = 0
        self._original_capture = None

        self._data = dict()

        # DroidCam URL
        # url = 'http://192.168.55.129:4747/video'
        url = 1
        self._capture_manager = CaptureManager(cv2.VideoCapture(url))
        self._window_manager = window_manager

    @property
    def original_capture(self):
        return self._original_capture

    @property
    def data(self):
        return self._data

    # from CaptureManager
    @property
    def processing_capture(self):
        return self._capture_manager.processed_frame

    @property
    def roi_capture(self):
        return self._capture_manager.roi_frame

    def release_frame(self):
        self._capture_manager.release_frame()

    # Thread
    @property
    def active(self):
        return not self._stopped

    @property
    def processed(self):
        return self._processed

    def start(self, face=0, count=100):
        print('Start recording')

        self._record_face = face
        self._record_count = count
        self._stopped = False

        # TODO: Thread Refactoring
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        self._processed = True
        self._amount_frames = 0
        self._success_finding_contours = 0

        while not self._stopped:
            self._capture_manager.enter_frame()

            original_capture = self._capture_manager.original_frame
            if original_capture is None:
                # self.stop()
                continue

            # (h, w) = original_capture.shape[:2]
            # center = (w / 2, h / 2)
            # M = cv2.getRotationMatrix2D(center, 270, 1.0)
            # self._original_capture = cv2.warpAffine(original_capture, M, (h, w))

            self._original_capture = original_capture

            self._amount_frames += 1

            height, width, _ = self._original_capture.shape

            self._capture_manager.processed_frame = self._original_capture.copy()
            cv2.rectangle(self._capture_manager.processed_frame,
                          (440, 300), (width-400, height-250), (0, 0, 255), 3)
            # cv2.rectangle(self._capture_manager.processed_frame,
            #               (80, 120), (width - 0, height - 260), (0, 0, 255), 3)

            self._capture_manager.roi_frame = self._original_capture[300:height-250, 440:width-400]
            # self._capture_manager.roi_frame = self._original_capture[120:height - 260, 80:width - 0]
            self._data[self._record_face * 10 + self._success_finding_contours] = self._capture_manager.roi_frame

            self._success_finding_contours += 1

            '''
            if self._capture_manager.roi_frame is None:
                self._capture_manager.roi_frame = self._original_capture

            # print("Recording: " + str(self._success_finding_contours))
            # print("Count: " + str(self._record_count))
            
            self._capture_manager.processed_frame, roi_frame = \
                processing.process_and_detect(self._original_capture, self._window_manager)

            if roi_frame is not None:
                self._capture_manager.roi_frame = roi_frame
                self._data[self._success_finding_contours * 10 + self._record_face] = self._capture_manager.roi_frame

                self._success_finding_contours += 1

                color_yellow = (0, 255, 255)
                percent_success_finding = round((self._success_finding_contours / self._amount_frames) * 100, 2)
                cv2.putText(self._capture_manager.processed_frame, str(percent_success_finding) + "%",
                            (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
                cv2.putText(self._capture_manager.processed_frame, str(self._success_finding_contours),
                            (15, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)
            '''

            self._capture_manager.exit_frame()

            if self._success_finding_contours >= self._record_count:
                print('Stop recording')
                self.stop()

        self._processed = False

    def stop(self):
        self._record_face = 0
        self._record_count = 0
        # self._data.clear()
        self._stopped = True

    def write_image(self, filename):
        self._capture_manager.write_image(filename)

    def is_writing_video(self):
        return self._capture_manager.is_writing_video

    def start_writing_video(self, filename):
        self._capture_manager.start_writing_video(filename)

    def stop_writing_video(self):
        self._capture_manager.stop_writing_video()
