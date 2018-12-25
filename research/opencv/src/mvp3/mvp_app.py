import cv2
import uart_control
import time
import pyttsx3
from window_manager import WindowManager
from imagedata_recorder import ImageDataRecorder


class SpeakerManager(object):
    """Provide a context to for using Speaker in with statements."""
    def __enter__(self):
        class Speaker(object):
            """Performs Text-To-Speech"""
            def __init__(self):
                self._engine = pyttsx3.init()
                voices = self._engine.getProperty('voices')
                for voice in voices:
                    if voice.languages[0] == u'ru_RU':
                        self._engine.setProperty('voice', voice.id)
                        break

                self._engine.startLoop(False)

            def say(self, message, pause):
                self._engine.say(message)
                start = time.time()
                while True:
                    self._engine.iterate()
                    duration = time.time() - start
                    if duration > pause:
                        break

            def cleanup(self):
                self._engine.endLoop()

        self.speaker = Speaker()
        return self.speaker

    def __exit__(self, type, value, traceback):
        self.speaker.cleanup()


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
        base_count = 5
        current_face = 1
        led = 10

        # with SpeakerManager() as speaker:
        #     speaker.say('Начинаем получение данных', 3)

        while current_face <= 4:
            # TODO:
            # uart.enable_led(led)]

            self._recorder.start(current_face, base_count)

            # TODO: show recording process, ...
            self._recorder_show()

            time.sleep(4)

            # uart.disable_led()

            # time.sleep(1)

            # TODO: rotate 90

            uart.start_step(1600)

            time.sleep(4)

            current_face += 1

        # how to wait: by keypress 's'
        # while not self._second_phase_activate:
        #    self._window_manager.process_events()

        with SpeakerManager() as speaker:
            speaker.say('Переверните упаковку', 3)

        time.sleep(10)

        # second phase: 2 faces
        while current_face <= 6:
            # TODO:
            # uart.enable_led(led)

            self._recorder.start(current_face, base_count)

            # TODO: show recording process, ...
            self._recorder_show()

            time.sleep(4)

            # uart.disable_led()

            # time.sleep(1)

            # TODO: rotate 180

            uart.start_step(3200)

            time.sleep(8)

            current_face += 1

        print(len(self._recorder.data))

        image_folder = './images/'
        for key in self._recorder.data.keys():
            image_filename = image_folder + 'image2_' + str(key) + '.png'
            print(image_filename)
            cv2.imwrite(image_filename, self._recorder.data[key])


if __name__ == "__main__":
    App().run_simple()
