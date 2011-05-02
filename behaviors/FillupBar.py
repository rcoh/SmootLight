from operationscore.Behavior import *
class FillupBar(Behavior):

    def processResponse(self, inputs, recurs):
        ret = []
        inputs = list(inputs)
        for inputset in inputs:
            inputset = dict(inputset)
            #Expecting SquareBlobMapper: ((x,y), distance)
            inputset['Location'] = ((inputset['Location'][0], 0), 10)
            ret.append(inputset)
        return (ret, [])

