from operationscore.Behavior import *
class Oval(Behavior):
    def processResponse(self, sensors, recurs):
        ret = []
        for data in sensors:
            #import pdb; pdb.set_trace()
            height = width = 1
            if 'Height' in self:
                height = 1/float(self['Height'])
            if 'Width' in self:
                width = 1/float(self['Width'])
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
            circleStr = \
                'math.sqrt((({x}-%(xLoc)d))**2*%(width)d+(({y}-%(yLoc)d)**2)*%(height)d)%(cond)s%(rad)d' % \
                locals() 
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
