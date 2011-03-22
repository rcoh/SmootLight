import pdb
import threading
import thread
import util.Config as configGetter
from operationscore.SmootCoreObject import SmootCoreObject
class ThreadedSmootCoreObject(SmootCoreObject, threading.Thread):
    """ThreadedSmootCoreObject is a version of SmootCoreObject for objects that want to run on their
    own thread"""
    def __init__(self, argDict, skipValidation = False):
        threading.Thread.__init__(self)
        SmootCoreObject.__init__(self, argDict, skipValidation)
        self.daemon = True #This kills this thread when the main thread stops
