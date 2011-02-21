from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class RunFinite(Behavior):
    """RunFinite will just wire input to output, but only a finite number of
    times as specified by the Iterations argument tag"""

    def behaviorInit(self):
        pass

    def processResponse(self, inp, state):

        if state:
            iterations = state
        else:
            iterations = self['Iterations']

        if iterations > 0:
            out = inp
        else:
            out = []

        iterations -= 1
        
        return (out, iterations)
