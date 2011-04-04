from operationscore.Behavior import *
import util.ColorOps as color
import pdb

class Boom(Behavior):        
    def processResponse(self, sInputs, rInputs):
        simpleOut = []
        recurOut = []
        
        for data in rInputs:
            if data['Radius'] > self['MaxRadius']:
                continue
            
            data['Radius'] += self['StepSize']
            xLoc = data['CenterLoc'][0]
            yLoc = data['CenterLoc'][1]
            rad = data['Radius']
            cond = '>=' if self['Outside'] else '<='
            circleStr = 'math.sqrt(({x}-'+str(xLoc)+')**2+(({y}-'+str(yLoc)+')**2))'+cond+str(rad)
            data['Location'] = circleStr

            simpleOut.append(data)            
            recurOut.append(data)
                        
        for data in sInputs:
            data['Radius'] = 1
            #import pdb; pdb.set_trace()
            if 'CenterLoc' in data:
                xLoc = data['CenterLoc'][0]
                yLoc = data['CenterLoc'][1]
            else:
                data['CenterLoc'] = tuple(data['Location'])
                xLoc = data['Location'][0]
                yLoc = data['Location'][1]

            #if not self['Id']+'Radius' in data:
            #    data[self['Id']+'Radius'] = self['Radius']
                
            rad = data['Radius']
            cond = '>=' if self['Outside'] else '<='
            circleStr = 'math.sqrt(({x}-'+str(xLoc)+')**2+(({y}-'+str(yLoc)+')**2))'+cond+str(rad)
            data['Location'] = circleStr
            data['Color'] = color.randomColor() 

            simpleOut.append(data)
            recurOut.append(data)
            
        return (simpleOut, recurOut)

    def setLastOutput(self, output):
        coutput = Behavior.deepCopyPacket(output)
        for data in coutput:
            data['Location'] = data['CenterLoc']
        return coutput
