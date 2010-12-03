import Util
import pdb
class SmootCoreObject:
    def __init__(self, argDict):
        self.argDict = argDict
        self.validateArgs(self.className()+'.params') 
        self.init() #call init of inheriting class
    #    self.__setitem__ = self.argDict.__setitem__
    #    self.__getitem__ = self.argDict.__getitem__
    def init(self):
        pass
    def className(self):
        return str(self.__class__).split('.')[-1]
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
