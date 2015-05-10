import glfw
from collections import defaultdict


class Input():
    def __init__(self):
        self.keyCounter = defaultdict(int)
        self.keyDown = defaultdict(bool)
        self.mouseButtonDown = defaultdict(bool)
        self.cursorPosition = [0, 0]

    def cursor_position_callback(self, window, x, y):
        self.cursorPosition = [x, y]

    def mouse_button_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.mouseButtonDown[button] = True
        elif action == glfw.RELEASE:
            self.mouseButtonDown[button] = False

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keyCounter[key] += 1
            self.keyDown[key] = True
        elif action == glfw.RELEASE:
            self.keyDown[key] = False
