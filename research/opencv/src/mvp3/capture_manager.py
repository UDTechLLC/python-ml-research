import cv2
import time


# TODO: camera parameters, like resolution, latency, fps (framerate, frame interval)
# TODO: best video processing
# TODO: image preprocessing, like decreasing/removing noise/shadows/blobs, enhancement, background substraction
class CaptureManager(object):
    def __init__(self, capture):
        self._capture = capture
        self._entered_frame = False

        self._original_frame = None
        self._processed_frame = None
        self._roi_frame = None

        self._image_filename = None
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None

        self._start_time = None
        self._frames_elapsed = int(0)
        self._fps_estimate = None

    @property
    def original_frame(self):
        if self._entered_frame and self._original_frame is None:
            _, self._original_frame = self._capture.retrieve()
        return self._original_frame

    @original_frame.setter
    def original_frame(self, value):
        self._original_frame = value

    @property
    def processed_frame(self):
        return self._processed_frame

    @processed_frame.setter
    def processed_frame(self, value):
        self._processed_frame = value

    @property
    def roi_frame(self):
        return self._roi_frame

    @roi_frame.setter
    def roi_frame(self, value):
        self._roi_frame = value

    @property
    def is_writing_image(self):
        return self._image_filename is not None

    @property
    def is_writing_video(self):
        return self._video_filename is not None

    def enter_frame(self):
        """Capture the next frame, if any."""

        # But first, check that any previous frame was exited.
        assert not self._entered_frame, \
            'previous enter_frame() had no matching exit_frame()'

        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exit_frame(self):
        """Draw to the window. Write to files. Release the frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.
        if self.original_frame is None:
            self._entered_frame = False
            return

        # Update the FPS estimate and related variables.
        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            time_elapsed = time.time() - self._start_time
            self._fps_estimate = self._frames_elapsed / time_elapsed
        self._frames_elapsed += 1

        self._entered_frame = False

    def release_frame(self):
        # Write to the image file, if any.
        if self.is_writing_image:
            cv2.imwrite(self._image_filename, self._processed_frame)
            self._image_filename = None

        # Write to the video file, if any.
        self._write_video_frame()

        # Release the frame.
        self._original_frame = None
        self._processed_frame = None
        # self._roi = None

    def write_image(self, filename):
        """Write the next exited frame to an image file."""
        self._image_filename = filename

    def start_writing_video(
            self, filename,
            encoding=cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')):
        """Start writing exited frames to a video file."""
        self._video_filename = filename
        self._video_encoding = encoding

    def stop_writing_video(self):
        """Stop writing exited frames to a video file."""
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._frames_elapsed < 20:
                    # Wait until more frames elapse so that the
                    # estimate is more stable.
                    return
                else:
                    fps = self._fps_estimate
            size = (int(self._capture.get(
                cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                        cv2.CAP_PROP_FRAME_HEIGHT)))
            self._video_writer = cv2.VideoWriter(
                self._video_filename, self._video_encoding,
                fps, size)

        self._video_writer.write(self._processed_frame)
