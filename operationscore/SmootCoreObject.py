import pdb
import threading
import thread
import util.Config as configGetter
import types

class SmootCoreObject(object):
    """SmootCoreObject is essentially a super-object class which grants us some niceties.  It allows
    us to use objects as if they are dictionaries -- we use this to store their arguments
    convienently -- note that querying for a parameter that does not exist will return None.  It
    also offers some basic ThreadSafety."""
    def __init__(self, argDict, skipValidation = False):
        self.dieListeners = []
        self.argDict = argDict
        self.validateArgs(self.className()+'.params') 
        self.lock = thread.allocate_lock()
        #put everything into attributes for speed
        for key in argDict:
            setattr(self, key, argDict[key])
        self.init() #call init of inheriting class
    
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
        
    def __getitem__(self, key):
        if key in self.argDict:
            item = self.argDict[key]
            if isinstance(item, types.FunctionType):
                return item(self.argDict) #resolve the lambda function, if it exists
            else:
                return item
        else:
            return None
    def __contains__(self, item):
        return item in self.argDict
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
