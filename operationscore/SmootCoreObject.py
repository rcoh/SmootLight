import pdb
import threading
import thread
import util.Config as configGetter

class SmootCoreObject(object):
    def __init__(self, argDict, skipValidation = False):
        self.dieListeners = []
        self.argDict = argDict
        self.validateArgs(self.className()+'.params') 
        self.lock = thread.allocate_lock()
        #put everything into attributes for speed
        for key in argDict:
            setattr(self, key, argDict[key])
        self.init() #call init of inheriting class
    #    self.__setitem__ = self.argDict.__setitem__
    #    self.__getitem__ = self.argDict.__getitem__
    
    def init(self):
        pass
        
    def acquireLock(self):
        self.lock = thread.allocate_lock() #TODO: fix. -- investigate this, it should only have to be run once in the initialization.
        self.lock.acquire()
        
    def releaseLock(self):
        self.lock.release()
        
    def className(self):
        return self.__class__.__name__
        
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
        self.validateArgDict(configGetter.loadParamRequirementDict(argFileName))#util
        #caches for us, woo!
        
    def validateArgDict(self, validationDict):
        for item in validationDict:
            if not item in self.argDict:
                raise Exception(validationDict[item])
    
    def addDieListener(self, listener):
        if listener not in self.dieListeners:
            self.dieListeners.append(listener)

    def removeDieListener(self, listener):
        if listener in self.dieListeners:
            self.dieListeners.remove(listener)    
        
    def die(self):
        for listener in self.dieListeners:
            listener.handleDie(self)
