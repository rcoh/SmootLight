import threading,time,Util
#Abstract class for inputs.  Inheriting classes should call "respond" to raise
#their event.  Inheriting classes MUST define sensingLoop.  Called at the
#interval specified in RefreshInterval while the input is active.  For example, if you are writing
#webserver, this is where the loop should go.
#Inheriting classes MAY define inputInit.  This is called before the loop
#begins.
import pdb
class Input(threading.Thread):
    #Event scope is a function pointer the function that will get called when
    #an Parent is raised.
    def __init__(self, argDict):
        self.eventQueue = []
        self.parentScope = argDict['parentScope']
        self.argDict = argDict
        if not 'InputId' in argDict:
            raise Exception('InputId must be defined in config xml')
        if not 'RefreshInterval' in argDict:
            print 'RefreshInterval not defined.  Defaulting to .5s.'
            self.argDict['RefreshInterval'] = 500 
        self.inputInit()
        threading.Thread.__init__(self)
        self.daemon = True #This kills this thread when the main thread stops
    def respond(self, eventDict):
        #if eventDict != []:
            #pdb.set_trace()
        self.parentScope.processResponse(self.argDict, eventDict)
    def newEvent(self, event): #Mostly just useful for grabbing events from the
        #computer running the sim (key presses, clicks etc.)
        self.eventQueue.append(event)
    def parentAlive(self):
        try:
            parentAlive = self.parentScope.alive()
            return parentAlive
        except:
            return False
    def run(self):
        while self.parentAlive():
            time.sleep(self.argDict['RefreshInterval']/float(1000))
            self.sensingLoop()
    def sensingLoop(self):
        pass
    def inputInit(self):
        pass


