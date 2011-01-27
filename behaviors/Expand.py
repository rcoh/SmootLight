from operationscore.Behavior import *
class Expand(Behavior):
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

