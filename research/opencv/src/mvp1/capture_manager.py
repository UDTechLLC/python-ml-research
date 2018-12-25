import cv2
import numpy
import time


class CaptureManager(object):
    def __init__(self, capture, preview_window_manager=None,
                 should_mirror_preview=False):

        self.previewWindowManager = preview_window_manager
        self.shouldMirrorPreview = should_mirror_preview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._original = None
        self._frame = None
        self._imageFilename = None
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = int(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame = None

    @property
    def original(self):
        if self._enteredFrame and self._original is None:
            _, self._original = self._capture.retrieve()
        return self._original

    @original.setter
    def original(self, value):
        self._original = value

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def is_writing_image(self):
        return self._imageFilename is not None

    @property
    def is_writing_video(self):
        return self._videoFilename is not None

    def enter_frame(self):
        """Capture the next frame, if any."""

        # But first, check that any previous frame was exited.
        assert not self._enteredFrame, \
            'previous enter_frame() had no matching exit_frame()'

        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exit_frame(self):
        """Draw to the window. Write to files. Release the frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.
        if self.original is None:
            self._enteredFrame = False
            return

        # Update the FPS estimate and related variables.
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Draw to the window, if any.
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(self._original, mirroredFrame)
            else:
                self.previewWindowManager.show(self._original, self._frame)

        # Write to the image file, if any.
        if self.is_writing_image:
            cv2.imwrite(self._imageFilename, self._frame)
            self._imageFilename = None

        # Write to the video file, if any.
        self._write_video_frame()

        # Release the frame.
        self._original = None
        self._frame = None
        self._enteredFrame = False

    def write_image(self, filename):
        """Write the next exited frame to an image file."""
        self._imageFilename = filename

    def start_writing_video(
            self, filename,
            encoding=cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')):
        """Start writing exited frames to a video file."""
        self._videoFilename = filename
        self._videoEncoding = encoding

    def stop_writing_video(self):
        """Stop writing exited frames to a video file."""
        self._videoFilename = None
        self._videoEncoding = None
        self._videoWriter = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._framesElapsed < 20:
                    # Wait until more frames elapse so that the
                    # estimate is more stable.
                    return
                else:
                    fps = self._fpsEstimate
            size = (int(self._capture.get(
                cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                        cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(
                self._videoFilename, self._videoEncoding,
                fps, size)

        self._videoWriter.write(self._frame)
