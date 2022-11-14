from dataclasses import dataclass
from pynput.mouse import Button
from pynput.keyboard import Key

FAILSAFE_KEY = Key.esc


@dataclass
class Input:
    code: any

    def __str__(self) -> str:
        return self.code.__str__()

    def is_mouse_code(self) -> bool:
        return type(self.code) is MouseCode

    def is_keyboard_code(self) -> bool:
        return type(self.code) is KeyboardCode


@dataclass
class MouseCode:
    x: int
    y: int
    button: Button
    pressed: bool

    def __str__(self) -> str:
        return "Mouse: {:6s} ({}, {})".format(self.button.name, self.x, self.y)


@dataclass
class KeyboardCode:
    key: Key

    def __str__(self):
        value: str = ""
        try:
            return "Board: {}".format(self.key.char)
        except AttributeError:
            return "Board: {}".format(self.key)
