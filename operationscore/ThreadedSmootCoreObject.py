import pdb
import threading
import thread
import util.Config as configGetter
from operationscore.SmootCoreObject import SmootCoreObject
class ThreadedSmootCoreObject(SmootCoreObject, threading.Thread):
    def __init__(self, argDict, skipValidation = False):
        self.argDict = argDict
        self.validateArgs(self.className()+'.params') 
        self.lock = thread.allocate_lock()
        threading.Thread.__init__(self)
        self.init() #call init of inheriting class
    #    self.__setitem__ = self.argDict.__setitem__
    #    self.__getitem__ = self.argDict.__getitem__
