#Abstract class for a behavior.  On every time step, the behavior is passed the
#inputs from all sensors it is bound to as well as any recursive inputs that it
#spawned during the last time step.  Inheriting classes MUST define
#processResponse.  processResponse should return a list of dictionaries which
#define the properties of the light response.  They must give a location and
#color.  They may define a function pointer which defines a custom mapping.
#[More on this later.  Bug Russell if you want to do it].
#recursiveResponse to queue a input on the next iteration with a dictionary
#argument.  This will be passed in via recursive inputs.
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
    def processResponse(self, sensorInputs, recursiveInputs):
        pass
    def addInput(self, sensorInput):
        self.sensorResponseQueue.append(sensorInput)
    #used for behavior chaining
    def immediateProcessInput(self, sensorInputs): 
        return self.processResponse(sensorInputs, [])
    def addInputs(self, sensorInputs):
        if type(sensorInputs) == type([]):
            [self.addInput(sensorInput) for sensorInput in sensorInputs]
        else:
            self.addInput(sensorInputs)
    def recursiveReponse(self, args):
        self.responseQueue.append(args)
    def timeStep(self):
        responses = self.processResponse(self.sensorResponseQueue, \
                self.recursiveResponseQueue)
        self.sensorResponseQueue = []
        self.recursiveResponseQueue = []
        return responses
