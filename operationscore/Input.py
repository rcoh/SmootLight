import threading,time
from logger import main_log, exception_log
from operationscore.ThreadedSmootCoreObject import ThreadedSmootCoreObject
import pdb
class Input(ThreadedSmootCoreObject):
    """Abstract class for inputs.  Inheriting classes should call "respond" to raise
    their event.  Inheriting classes MUST define sensingLoop.  Called at the
    interval specified in RefreshInterval while the input is active.  For example, if you are writing
    webserver, this is where the loop should go.
    Inheriting classes MAY define inputInit.  This is called before the loop
    begins."""
    def init(self):
        self.eventQueue = []
        if not 'RefreshInterval' in self.argDict:
            self.argDict['RefreshInterval'] = 500 
        self.parentScope = self.argDict['parentScope']
        self.inputInit()
        
    def respond(self, eventDict):
        #if eventDict != []:
        self.parentScope.lock.acquire()
        self.parentScope.processResponse(self.argDict, eventDict)
        self.parentScope.lock.release()
        time.sleep(.001)
        
    def parentAlive(self):
        try:
            parentAlive = self.parentScope.alive()
            return parentAlive
        except:
            return False
            
    def run(self):
        while 1:
            try:
                die = self.parentAlive()
            except:
                break
            time.sleep(self.argDict['RefreshInterval']/float(1000))
            self.acquireLock()
            self.sensingLoop()
            self.releaseLock()
            
    def sensingLoop(self):
        pass
        
    def inputInit(self):
        pass


