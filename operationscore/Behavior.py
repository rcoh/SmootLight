#Abstract class for a behavior.  On every time step, the behavior is passed the
#inputs from all sensors it is bound to as well as any recursive inputs that it
#spawned during the last time step.  Inheriting classes MUST define
#processResponse.  processResponse should return a list of dictionaries which
#define the properties of the light response, (outputs, recursions).  They must give a location and
#color.  They may define a PixelEvent to more closely control the outgoing
#data, however, this is normally handled by routing the event to a behavior
#specifically designed to do this (like DecayBehavior). 

import pdb
from operationscore.SmootCoreObject import *
#timeStep is called on every iteration of the LightInstallation
#addInput is called on each individual input received, and the inputs queue
class Behavior(SmootCoreObject):
    def init(self):
        self.validateArgs('Behavior.params')
        if type(self['Inputs']) != type([]):
            self['Inputs'] = [self['Inputs']]
        self.recursiveResponseQueue = []
        self.sensorResponseQueue = []
        self.outGoingQueue = []
        self.behaviorInit()
    def behaviorInit(self):
        pass
    def processResponse(self, sensorInputs, recursiveInputs):
        pass
    def addInput(self, sensorInput):
        self.sensorResponseQueue.append(sensorInput)
    #used for behavior chaining
    def immediateProcessInput(self, sensorInputs, recursiveInputs=[]): 
        try:
            (output,recursions) = self.processResponse(sensorInputs, \
                    recursiveInputs)
            if type(output) != type([]):
                output = [output]
            return (output, recursions)
        except:
            return (self.processResponse(sensorInputs, recursiveInputs),[])
    def addInputs(self, sensorInputs):
        if type(sensorInputs) == type([]):
            [self.addInput(sensorInput) for sensorInput in sensorInputs]
        else:
            self.addInput(sensorInputs)
    def timeStep(self):
        responses = self.processResponse(self.sensorResponseQueue, \
                self.recursiveResponseQueue)
        if type(responses) == type(tuple()) and len(responses) == 2:
            (outputs, recursions) = responses
        else:
            outputs = responses
            recursions = []
        self.sensorResponseQueue = []
        self.recursiveResponseQueue = recursions 
        if type(outputs) != type([]):
            outputs = [outputs]
        try:
            return outputs
        except:
            pass
            #pdb.set_trace()
        return outputs 
