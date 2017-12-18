
from time import sleep
from ui import Ui
from controller import Controller

class Minispice(object):
    def __init__(self):
        self.ui = Ui()
        self.controller = Controller()

    def run(self):
        # Start threads
        self.ui.start()
        self.controller.start()

        while True:
            sleep(0.01)

if __name__ == "__main__":
    ms = Minispice()
    ms.run()
