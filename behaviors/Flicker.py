from operationscore.Behavior import *
import util.ComponentRegistry as compReg
from logger import main_log
import random
class Flicker (Behavior):
    """Flicker will drop inputs or whole frames with a certain probability, 
    given by the parameter Prob and AllProb, decimals from 0 to 1, where 1 
    means all inputs/frames pass through and 0 means all inputs/frames are 
    dropped."""

    def processResponse(self, inputs, state):
        out = []

        if len(state):
            state0 = state[0]
            p = state0['p']
            ap = state0['ap']
        else:
            p = self['Prob']
            ap = self['AllProb']
            state = [{'p':p, 'ap':ap}]

        if random.random() <= ap:
            for inp in inputs:
                if random.random() <= p:
                    out[0:0] = [inp]

        return (out, state)


