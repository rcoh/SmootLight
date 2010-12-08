import Util
import pdb
import threading
import thread
class SmootCoreObject(threading.Thread):
    def __init__(self, argDict, skipValidation = False):
        self.argDict = argDict
        self.validateArgs(self.className()+'.params') 
        self.lock = thread.allocate_lock()
        self.init() #call init of inheriting class
    #    self.__setitem__ = self.argDict.__setitem__
    #    self.__getitem__ = self.argDict.__getitem__
    def init(self):
        pass
    def acquireLock(self):
        self.lock = thread.allocate_lock() #TODO: fix.
        self.lock.acquire()
    def releaseLock(self):
        self.lock.release()
    def className(self):
        return str(self.__class__).split('.')[-1] #TODO: this doesn't work.
    def __setitem__(self,k, item):
        self.argDict[k] = item
    def __getitem__(self, item):
        if item in self.argDict:
            return self.argDict[item]
        else:
            return None
    def __getiter__(self):
        return self.argDict.__getiter__()
    def validateArgs(self, argFileName):
        self.validateArgDict(Util.loadParamRequirementDict(argFileName))#util
        #caches for us, woo!
    def validateArgDict(self, validationDict):
        for item in validationDict:
            if not item in self.argDict:
                raise Exception(validationDict[item])
