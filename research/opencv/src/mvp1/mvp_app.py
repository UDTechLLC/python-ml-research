import cv2
from window_manager import WindowManager
from capture_manager import CaptureManager
from multiprocessing.pool import ThreadPool
from collections import deque


# import filters
# import image_processor
# import object_detector


class DummyTask:
    def __init__(self, data):
        self.data = data

    def ready(self):
        return True

    def get(self):
        return self.data


class MVP(object):
    def __init__(self):
        self._thread_mode = True

        self._windowManager = WindowManager('Minimum Viable Product',
                                            self.on_keypress)

        self._amount_frames = 0
        self._success_finding_contours = 0
        # DroidCam URL
        # url = 'http://192.168.55.78:4747/video'
        url = 0
        self._captureManager = CaptureManager(
            cv2.VideoCapture(url), self._windowManager, False)

        # self._curveFilter = filters.BGRPortraCurveFilter()
        # self._convolutionFilter = filters.FindEdgesFilter()
        # self._imageProcessor = image_processor.SimpleImageProcessor()
        # self._objectDetector = object_detector.SimpleObjectDetector()

    def run(self):
        """Run the main loop."""

        threadn = cv2.getNumberOfCPUs()
        pool = ThreadPool(processes=threadn)
        pending = deque()

        # latency = StatValue()
        # frame_interval = StatValue()
        # last_frame_time = clock()

        # TODO: Camera Calibration, Video Stabilization

        self._windowManager.create_window()

        while self._windowManager.is_window_created:
            self._captureManager.enter_frame()
            original = self._captureManager.original
            self._captureManager.frame = original

            # if original is not None:
            #    output = self.process_and_detect(original)
            #    self._captureManager.frame = output§

            while len(pending) > 0 and pending[0].ready():
                output = pending.popleft().get()
                # latency.update(clock() - t0)
                cv2.putText(output, "threaded      :  " + str(self._thread_mode),
                            (15, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                # draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value * 1000))
                # draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value * 1000))
                self._captureManager.frame = output
                self._captureManager.exit_frame()

            if len(pending) < threadn:
                # ret, frame = cap.read()
                # t = clock()
                # frame_interval.update(t - last_frame_time)
                # last_frame_time = t
                if self._thread_mode:
                    task = pool.apply_async(self.process_and_detect, (original.copy(),))
                else:
                    task = DummyTask(self.process_and_detect(original))
                pending.append(task)

            self._captureManager.exit_frame()
            self._windowManager.process_events()

    def process_and_detect(self, src):
        self._amount_frames += 1
        # filters.strokeEdges(src, src)
        # self._curveFilter.apply(src, src)
        # self._convolutionFilter.apply(src, src)
        # self._imageProcessor.process(src, src)
        # self._objectDetector.detect(src)

        # TODO: Image Preprocessor: removing shadows, small blobs, noise, enhancing, etc

        # TODO: Image Processor
        processing = self.image_processing_template_one(src)
        # gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        # filtering = cv2.bilateralFilter(gray, 1, 10, 120)

        # TODO: Object Detector
        output = cv2.cvtColor(processing, cv2.COLOR_GRAY2BGR)
        success_detect = self.try_detect(input=processing, output=output, post_detect_fn=self.post_detect_draw)

        if not success_detect:
            # TODO: image_processing_template_two
            pass

        # TODO: Get 4-contours square counts If zero
        # TODO: [For 3D] Wrapping & Transformations

        # TODO: to be continued
        return output

    def image_processing_template_one(self, src):
        # TODO: Color space: GRAYSCALE, HSV, ...
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        # TODO: Convolution, Blurring, ...
        # filtering = cv2.bilateralFilter(gray, 1, 10, 120)
        filtering = self.image_filtering(gray)

        # TODO: Edge detection
        # edges = cv2.Canny(gray, 10, 250)
        edges = self.edge_detection(filtering)

        # TODO: Morphological operations
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        # closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        closed = self.morphological_transformations(edges)
        return closed

    def image_filtering(self, src):
        diameter = self._windowManager.get_trackbar_value('diameter(for bilateralFilter)')
        sigma_color = self._windowManager.get_trackbar_value('sigmaColor(for bilateralFilter)')
        sigma_space = self._windowManager.get_trackbar_value('sigmaSpace(for bilateralFilter)')
        filtering = cv2.bilateralFilter(src, diameter, sigma_color, sigma_space)
        return filtering

    def edge_detection(self, src):
        threshold_min = self._windowManager.get_trackbar_value('threshold min(for Canny edge detection)')
        threshold_max = self._windowManager.get_trackbar_value('threshold max(for Canny edge detection)')
        edges = cv2.Canny(src, threshold_min, threshold_max)
        return edges

    def morphological_transformations(self, edges):
        kernel_size = self._windowManager.get_trackbar_value('kernel size(morphological structuring element)')
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        return closed

    def try_detect(self, input, output, post_detect_fn):
        success_standard = self.detect_standard_rects(input, output, post_detect_fn)
        if not success_standard:
            # TODO: detect_rects_by_lines
            pass

        return success_standard

    def detect_standard_rects(self, input, output, post_detect_fn):
        contour_area_points = self._windowManager.get_trackbar_value('Contour area min amount points (*100)')
        approx_edges_amount = self._windowManager.get_trackbar_value('Approx edges amount')

        _, contours, h = cv2.findContours(input, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rects_count = 0
        for cont in contours:
            if cv2.contourArea(cont) > contour_area_points * 100:
                arc_len = cv2.arcLength(cont, True)
                approx = cv2.approxPolyDP(cont, 0.1 * arc_len, True)
                if len(approx) == approx_edges_amount:
                    post_detect_fn(output, approx)
                    rects_count += 1

        if rects_count > 0:
            self._success_finding_contours += 1

        color_yellow = (0, 255, 255)
        percent_success_finding = round((self._success_finding_contours / self._amount_frames) * 100, 2)
        cv2.putText(output, str(percent_success_finding) + "%",
                    (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)

        return rects_count > 0

    @staticmethod
    def post_detect_draw(output, approx):
        cv2.drawContours(output, [approx], -1, (255, 0, 0), 2)

    def on_keypress(self, keycode):
        """Handle a keypress.

        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.

        """
        if keycode == 32:  # space
            # self._captureManager.write_image('screenshot.png')
            self._thread_mode = not self._thread_mode
        elif keycode == 9:  # tab
            if not self._captureManager.is_writing_video:
                self._captureManager.start_writing_video(
                    'screencast.avi')
            else:
                self._captureManager.stop_writing_video()
        elif keycode == 27:  # escape
            self._windowManager.destroy_window()


if __name__ == "__main__":
    MVP().run()
