from operationscore.Behavior import *
class FillupBar(Behavior):

    def processResponse(self, inputs, recurs):
        ret = []
        inputs = list(inputs)
        for inputset in inputs:
            inputset = dict(inputset)
            #Expecting SquareBlobMapper: ((x,y), distance)
            #50 was chosen so that the initial square is tall enough to fill up the bar vertically.
            inputset['Location'] = ((inputset['Location'][0], 50), 10)
            ret.append(inputset)
        return (ret, [])

