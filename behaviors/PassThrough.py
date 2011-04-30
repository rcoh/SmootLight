from operationscore.Behavior import *

class PassThrough(Behavior):

    def processResponse (self, inputs, state):
        
        return (inputs, state) 
