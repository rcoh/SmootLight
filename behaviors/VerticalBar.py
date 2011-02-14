from operationscore.Behavior import *
class VerticalBar(Behavior):

    def processResponse(self, inputs, recurs):
        ret = []
        inputs = list(inputs)
        for inputset in inputs:
            #import pdb; pdb.set_trace()
            inputset = dict(inputset) 
            if 'xLoc' not in inputset:
                inputset['xLoc'] = inputset['Location'][0]
            xLoc = inputset['xLoc']

            condition = '{x} == ' + str(xLoc)
            
            if self['Combine']:
                inputset['Location'] += ',' + condition
            else:
                inputset['Location'] = condition 

            ret.append(inputset)
        return (ret, [])

