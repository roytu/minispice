
"""
    ui = UI()
    ui.run()

    In loop:
        ui.add(Ui_Rect(x, y, w, h), depth=-1)
        ui.add(Ui_Text(x, y, text), depth=-2)
"""

import sys
import os
from time import sleep
from threading import Thread, Event

RHAPSODY_TEXT = """This is a test!
For the next 50 seconds this station will conduct a test
Of the emergency broadcast system!
This is only a test!

- Rhapsody
"""


""" BEGIN UI OBJECTS """
class Ui_Rect(object):
    def __init__(self, x, y, w, h, fill=None, text=None, text_margin=2):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.fill = fill
        self.text = text
        self.text_margin = text_margin

    def imprint(self, ui_w, ui_h, s):
        """ Take a UI string and imprint your string onto it
            @ui_w: UI width
            @ui_h: UI height
        """
        text_left = self.text
        for y_ in range(self.y, self.y + self.h):
            first = (y_ == self.y)
            last = (y_ == self.y + self.h - 1)

            start = y_ * (ui_w + 0) + self.x  # -1, 0, +1
            end = start + self.w

            if self.fill:
                line = self.fill * self.w
            else:
                if first:
                    line = "/" + "-" * (self.w - 2) + "\\"
                elif last:
                    line = "\\" + "-" * (self.w - 2) + "/"
                else:
                    line = ""
                    line += "|"
                    if text_left:
                        lst = text_left.split("\n")
                        a = lst.pop(0)
                        text_left = "\n".join(lst)

                        line += " " * self.text_margin
                        line += a.ljust(self.w - 2 - self.text_margin * 2, " ")
                        line += " " * self.text_margin
                    else:
                        line += " " * (self.w - 2)
                    line += "|"
            
            s = s[:start] + line + s[end:]
        return s

""" END UI OBJECTS """

""" Interface-like Ui object """
class Ui_Object(object):
    def __init__(self):
        pass

    def draw(self):
        """ Override this """
        pass

class Ui(Thread):
    """ Maintain a list of UI Objects and print them
        to screen in a funny way
    """
    def __init__(self, w=None, h=None):
        Thread.__init__(self)
        self.stop_event = Event()
        self.daemon = True

        self.ui_objects = []
        if w is None or h is None:
            w, h = self.get_size()
        self.w = w
        self.h = h

        self.add(Ui_Rect(2, 2, 80, 10, text=RHAPSODY_TEXT))

    def get_size(self):
        h, w = os.popen('stty size', 'r').read().split()
        h, w = int(h), int(w)
        return (w, h)

    def add(self, ui_obj, depth=0):
        # TODO depth
        self.ui_objects.append(ui_obj)

    def draw(self):
        # Initialize empty screen

        # TODO optimize this eventually
        self.w, self.h = self.get_size()

        s = ""
        s += "u" * (self.w - 1) + "\n"
        for _ in range(self.h - 2):
            s += "l"
            s += " " * (self.w - 3)
            s += "r"
            s += "\n"
        s += "d" * (self.w - 1)

        # Add the dudes
        for ui_obj in self.ui_objects:
            s = ui_obj.imprint(self.w, self.h, s)

        sys.stdout.flush()
        sys.stdout.write(s)

    def run(self):
        while not self.stop_event.is_set():
            self.draw()
            sleep(0.1)

if __name__ == "__main__":
    ui = Ui()
    ui.add(Ui_Rect(2, 2, 80, 10, text=text))
    ui.run()
