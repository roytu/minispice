
"""
    ui = UI()
    ui.run()

    In loop:
        ui.add(Ui_Rect(x, y, w, h, depth=-1))
        ui.add(Ui_Text(x, y, depth=0, text))
"""

import sys
import os
from time import sleep

class Ui_Rect(object):
    def __init__(self, x, y, w, h, depth=0):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.depth = depth  # Lower depth in front

    def draw(self, s):
        """ Take a UI string and do the thing to it """
        # TODO x, y

        s += "=" * self.w
        s += "\n"
        for _ in range(self.h-2):
            s += "|"
            s += " " * (self.w-2)
            s += "|"
            s += "\n"
        s += "=" * self.w
        s += "\n"

        return s

class Ui_Object(object):
    def __init__(self, depth=0):
        self.depth = depth  # Lower depth in front

    def drawable(self):
        """ Override this """
        pass

class Ui(object):
    """ Maintain a list of UI Objects and print them
        to screen in a funny way
    """
    def __init__(self, w=None, h=None):
        self.ui_objects = []
        if w is None or h is None:
            h, w = os.popen('stty size', 'r').read().split()
            h, w = int(h), int(w)
        self.w = w
        self.h = h

    def add(self, ui_obj):
        self.ui_objects.append(ui_obj)

    def draw(self):
        # Initialize empty screen
        s = ("A" * self.w + "\n") * self.h

        # Add the dudes
        for ui_obj in self.ui_objects:
            s = ui_obj.draw(s)

        sys.stdout.flush()
        sys.stdout.write(s)

    def run(self):
        while True:
            self.draw()
            sleep(1)

if __name__ == "__main__":
    ui = Ui()
    ui.add(Ui_Rect(10, 10, 20, 20))
    ui.run()
