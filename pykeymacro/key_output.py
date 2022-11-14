import time
from typing import Callable
from pynput import mouse, keyboard
from pynput.keyboard import Key
from input_code import Input, MouseCode, KeyboardCode, FAILSAFE_KEY


class KeyOutput:

    def __init__(self, callback: Callable[[None], None]) -> None:
        self.callback = callback
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.keyboard_listener = None

    def start_output(self, record_list: list[Input], interval: int = 0, isLoop: bool = False):
        self.is_running = True
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_keyboard_press)
        self.keyboard_listener.start()
        sleep_time_list = self.__create_sleep_time_list(interval)

        while True:
            if not self.is_running:
                break
            for record in record_list:
                if not self.is_running:
                    break
                if record.is_mouse_code():
                    self.__on_mouse(record.code)
                elif record.is_keyboard_code():
                    self.__on_key(record.code)
                for sleep_time in sleep_time_list:
                    if not self.is_running:
                        break
                    time.sleep(sleep_time)
            if not isLoop:
                break
        self.stop_output()
        self.callback()

    def stop_output(self):
        self.is_running = False
        self.keyboard_listener.stop()

    def __on_keyboard_press(self, key: Key):
        if key == FAILSAFE_KEY:
            print("Input failsafe key")
            self.is_running = False

    def __create_sleep_time_list(self, interval: int) -> list[float]:
        seconds = float(interval) / 1000
        integer = seconds // 1
        decimal = seconds % 1
        result = [1.0] * int(integer)
        if decimal != 0.0:
            result.append(decimal)
        return result

    def __on_mouse(self, code: MouseCode):
        self.mouse_controller.position = (code.x, code.y)
        self.mouse_controller.press(code.button)
        self.mouse_controller.release(code.button)

    def __on_key(self, code: KeyboardCode):
        self.keyboard_controller.press(code.key)
        self.keyboard_controller.release(code.key)
