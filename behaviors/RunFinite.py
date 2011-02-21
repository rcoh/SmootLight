from operationscore.Behavior import *
import util.ComponentRegistry as compReg

class RunFinite(Behavior):
    """RunFinite will just wire input to output, but only a finite number of
    times as specified by the Iterations argument tag"""

    def behaviorInit(self):
        pass

    def processResponse(self, inp, state):

        print "runfinite ", str(inp), ",", str(state)
        if state != []:
            iterations = state
        else:
            iterations = self['Iterations']

        if iterations > 0:
            out = inp
        else:
            out = []

        if inp:
            iterations -= 1

        print "  -->", str(iterations), ",", str(out)
        return (out, iterations)
