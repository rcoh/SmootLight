from operationscore.Behavior import *

class DiscardData(Behavior):
    """DiscardData will discard all input packets except for the first n
    packets, where n is denoted by <Keep>"""

    def processResponse(self, inputs, state):
        if len(inputs) > self['Keep']:
            return (inputs[-self['Keep']:], state)
        else:
            return (inputs, state)
