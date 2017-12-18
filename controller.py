
from threading import Thread, Event
from getch import getch

class ControllerState(object):
    """ Passable state by Controller to Ui """
    pass

class Controller(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stop_event = Event()
        self.daemon = True

        self.state = ControllerState()

    def run(self):
        while not self.stop_event.is_set():
            c = getch()
            if c == "q":
                self.stop_event.set()

        pass
