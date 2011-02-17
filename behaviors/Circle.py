from operationscore.Behavior import *
class Circle(Behavior):
    def processResponse(self, sensors, recurs):
        ret = []
        for data in sensors:
            #import pdb; pdb.set_trace()
            if 'CenterLoc' in data:
                xLoc = data['CenterLoc'][0]
                yLoc = data['CenterLoc'][1]
            else:
                data['CenterLoc'] = tuple(data['Location'])
                xLoc = data['Location'][0]
                yLoc = data['Location'][1]
            if not self['Id']+'Radius' in data:
                data[self['Id']+'Radius'] = self['Radius']
            rad = data[self['Id']+'Radius']
            cond = '>=' if self['Outside'] else '<='
            circleStr = 'math.sqrt(({x}-'+str(xLoc)+')**2+(({y}-'+str(yLoc)+')**2))'+cond+str(rad)
            if self['Combine']:
                data['Location'] += ',' + circleStr
            else:
                data['Location'] = circleStr 
            ret.append(data)
        return (ret, [])
    def setLastOutput(self, output):
        coutput = Behavior.deepCopyPacket(output)
        for data in coutput:
            data['Location'] = data['CenterLoc']
        return coutput
