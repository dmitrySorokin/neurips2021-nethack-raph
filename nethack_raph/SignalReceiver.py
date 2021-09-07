import inspect
from nethack_raph.Kernel import *


class SignalReceiver:
    def __init__(self):
        self.kernel().addSignalReceiver(self)

    def signal(self, s, *args, **args2):
        for x in inspect.getmembers(self):
            if x[0] == s:
                x[1](*args, **args2)
