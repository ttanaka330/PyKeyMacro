from typing import Callable
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
from input_code import Input, MouseCode, KeyboardCode, FAILSAFE_KEY


class KeyInput:

    def __init__(self, callback: Callable[[Input], None]) -> None:
        self.callback = callback
        self.mouse_listener = None
        self.keyboard_listener = None

    def start_input(self):
        self.stop_input()

        self.mouse_listener = mouse.Listener(
            on_move=self.__on_mouse_move,
            on_click=self.__on_mouse_click,
            on_scroll=self.__on_mouse_scroll)
        self.keyboard_listener = keyboard.Listener(
            on_press=self.__on_keyboard_press,
            on_release=self.__on_keyboard_release)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop_input(self):
        if self.mouse_listener is not None and self.mouse_listener.running:
            self.mouse_listener.stop()
        self.mouse_listener = None

        if self.keyboard_listener is not None and self.keyboard_listener.running:
            self.keyboard_listener.stop()
        self.keyboard_listener = None

    def __on_mouse_move(self, x: int, y: int):
        pass  # 未対応

    def __on_mouse_click(self, x: int, y: int, button: Button, pressed: bool):
        if pressed:
            result = MouseCode(x=x, y=y, button=button, pressed=pressed)
            self.callback(Input(code=result))

    def __on_mouse_scroll(self, x: int, y: int, dx: int, dy: int):
        pass  # 未対応

    def __on_keyboard_press(self, key: Key):
        if key == FAILSAFE_KEY:
            return
        result = KeyboardCode(key=key)
        self.callback(Input(code=result))

    def __on_keyboard_release(self, key: Key):
        pass  # 未対応
