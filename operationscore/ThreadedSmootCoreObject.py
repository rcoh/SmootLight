import pdb
import threading
import thread
import util.Config as configGetter
from operationscore.SmootCoreObject import SmootCoreObject
class ThreadedSmootCoreObject(SmootCoreObject, threading.Thread):
    def __init__(self, argDict, skipValidation = False):
        SmootCoreObject.__init__(self, argDict, skipValidation)
        threading.Thread.__init__(self)
        self.daemon = True #This kills this thread when the main thread stops
