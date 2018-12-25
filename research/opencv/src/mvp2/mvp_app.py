import uart_control
import time
from window_manager import WindowManager
from imagedata_recorder import ImageDataRecorder


class App(object):
    def __init__(self):
        self._window_manager = WindowManager('Minimum Viable Product', self._on_keypress)
        self._recorder = ImageDataRecorder(self._window_manager)
        self._second_phase_activate = False

    def _on_keypress(self, keycode):
        """Handle a keypress.

        space  -> Take a screenshot.
        tab    -> Start/stop recording a screencast.
        escape -> Quit.

        """
        if keycode == 32:  # space
            self._recorder.write_image('screenshot.png')
        elif keycode == 9:  # tab
            if not self._recorder.is_writing_video:
                self._recorder.start_writing_video(
                    'screencast.avi')
            else:
                self._recorder.stop_writing_video()
        elif keycode == 27:  # escape
            self._recorder.stop()
            while self._recorder.processed:
                pass
                self._window_manager.destroy_window()
        elif keycode == 115:  # s
            self._second_phase_activate = True
        else:
            print(keycode)

    def _recorder_show(self):
        while self._recorder.processed and self._window_manager.is_window_created:
            self._window_manager.process_events()

            original = self._recorder.original_capture
            processing = self._recorder.processing_capture
            roi = self._recorder.roi_capture

            self._window_manager.show(original, processing, roi)

            self._recorder.release_frame()

    def run_simple(self):
        self._window_manager.create_window()

        self._recorder.start(0, 1000)
        self._recorder_show()

    def run_algorithm(self):
        self._window_manager.create_window()
        uart = uart_control.UartControl()

        # first phase: 4 faces
        base_count = 3
        current_face = 0
        led = 10

        while current_face < 4:
            # TODO:
            uart.enable_led(led)

            self._recorder.start(current_face, base_count)

            # TODO: show recording process, ...
            self._recorder_show()

            time.sleep(4)

            uart.disable_led()

            time.sleep(1)

            # TODO: rotate 90

            uart.start_step(1600)

            time.sleep(4)

            current_face += 1

        # how to wait: by keypress 's'
        #while not self._second_phase_activate:
        #    self._window_manager.process_events()

        time.sleep(10)

        # second phase: 2 faces
        while current_face < 6:
            # TODO:
            uart.enable_led(led)

            self._recorder.start(current_face, base_count)

            # TODO: show recording process, ...
            self._recorder_show()

            time.sleep(4)

            uart.disable_led()

            time.sleep(1)

            # TODO: rotate 180

            uart.start_step(3200)

            time.sleep(8)

            current_face += 1

        # print(len(self._recorder.data))

    def test_uart(self):
        uart = uart_control.UartControl()
        uart.enable_led(10)
        uart.start_step(6400)
        time.sleep(12.8)
        uart.disable_led()

        # ser = serial.Serial()
        # ser.port = "/dev/ttyUSB0"
        # ser.baudrate = 9600
        # ser.parity = serial.PARITY_NONE
        # ser.timeout = 5
        #
        # ser.open()
        # ser.flushInput()
        # ser.flushOutput()
        # i = ser.write(b'st\r\n')
        # print(i)
        #
        # time.sleep(5)
        #
        # line = ser.readline()
        # print(line)


if __name__ == "__main__":
    App().run_algorithm()
