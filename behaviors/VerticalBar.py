from operationscore.Behavior import *
class VerticalBar(Behavior):

    def processResponse(self, inputs, recurs):

        ret = []
        for inputset in inputs:
            #import pdb; pdb.set_trace()
            
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

    def setLastOutput(self, output):

        coutput = Behavior.deepCopyPacket(output)
        for data in coutput:
            data['Location'] = data['xLoc']
        return coutput
