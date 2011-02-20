from operationscore.Behavior import *

class LocationMask (Behavior):
    """Modifies Pixels such that only ones in the pixels specified by the "location"
    argument will show"""

    def processResponse(self, inputs, state):

        ret = []
        inputs = list(inputs)

        for inputset in inputs:
            inputset = dict(inputset)

            inputset['Location'] += '@' + self['Location']

            ret.append(inputset)

        return (ret, [])
