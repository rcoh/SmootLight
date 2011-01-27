from operationscore.Behavior import *
class Expand(Behavior):
    """Expand is a behavior that generates a response that grows horizontally starting a location
    specifed in input.  Required Args:
    <ExpandRate>123</ExpandRate> which is the expandrate in units/response"""

    def processResponse(self, sensorInputs, recurs):
        ret = []
        for data in sensorInputs:
            if not 'Left' in data: #If this is the first time we have seen this input
                data['Left'] = data['Location'][0]
                data['Right'] = data['Location'][0]
                data['ExpandRate'] = self['ExpandRate']

            data = dict(data)
            data['Left'] -= data['ExpandRate']
            data['Right'] += data['ExpandRate']
            data['Location'] = "{x}>" + str(data['Left']) + ", {x}<" + str(data['Right'])
            ret.append(data)
        return (ret, [])

