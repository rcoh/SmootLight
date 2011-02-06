from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.ColorOps as colorOps
from pixelevents.RandomEvent import *
class ColorCompetition(Behavior):
    """ColorCompetition is a behavior that takes a number from 1 to 100 and makes a white line down
    the middle of the display.  Requires:
    <MaxInput> -- system expects input from 0 to MaxInput
    <CenterWidth> -- the width of the central bar
    <LeftColor> -- the left color
    <RightColor> -- the right color
    <LineHeight> -- the height of the lines
    """
    def behaviorInit(self):
        self.mode = '@'
    def processResponse(self, sensors, recurses):
        #1st, grab the last item in sensors
        if sensors:
            sensorStr = sensors[-1]['Data']
            if 'win' in sensorStr:
                self.mode = sensorStr
            else:
                self['parentScope'].refreshInterval = 30
                self.mode = sensors[-1]['Data'][0]
                sensors[-1]['Data'] = sensors[-1]['Data'][1:] 
        if self.mode == '@':
            return self.game1(sensors, recurses)
        if self.mode == '#':
            return self.game2(sensors, recurses)
        if self.mode == '$':
            return self.game3(sensors, recurses)
        if self.mode == '%':
            return self.game4(sensors, recurses)
        if self.mode == '&':
            return self.game5(sensors, recurses)
        if 'win' in self.mode:
            return self.win()
    def game1(self, sensors, recurses):
        if sensors:
            sensorStr = sensors[-1]['Data']
            (lineLocation, intensityL, intensityR) = eval(sensors[-1]['Data'])
        elif recurses:
            (lineLocation, intensityL, intensityR) = recurses[-1]['Data']
        else:
            (lineLocation, intensityL, intensityR) = (self['MaxInput'] / 2,0,0)
        return self.competition(lineLocation, intensityL, intensityR)

    def competition(self,lineLocation, intensityL, intensityR):
        ret = []
        screenWidth = compReg.getComponent('Screen').getSize()[2]
        scaleFactor = screenWidth / float(self['MaxInput'])

        leftBound = lineLocation-self['CenterWidth']/2.
        rightBound = lineLocation+self['CenterWidth']/2.
        
        leftBound *= scaleFactor
        rightBound *= scaleFactor 
        leftBound -= 1
        rightBound += 1
        lColor = colorOps.multiplyColor(self['LeftColor'], 1+intensityL) 
        rColor = colorOps.multiplyColor(self['RightColor'], 1+intensityR) 
        ret.append({'Color':lColor, 'Location':'{x}<'+str(leftBound)})
        ret.append({'Color':(255,255,255), 'Location':'{x}>'+str(leftBound) + \
                    ', {x}<'+str(rightBound)})
        ret.append({'Color':rColor, 'Location':'{x}>'+str(rightBound)})

        return (ret, [{'Data': (lineLocation, intensityL, intensityR)}])
    def game2(self, sensors, recurses):
        if sensors:
            (l, r, intensityL, intensityR) = eval(sensors[-1]['Data'])
        elif recurses:
            if len(recurses[-1]['Data']) != 4:
                   return ([], []) #if we are getting behavior-interference
            (l, r, intensityL, intensityR) = recurses[-1]['Data']
        else:
            (l, r, intensityL, intensityR) = (0,0,0,0)
        
        return self.mix(l,r,intensityL, intensityR)
    def mix(self, l,r,intensityL,intensityR):
        screenWidth = compReg.getComponent('Screen').getSize()[2]
        scaleFactor = screenWidth / float(self['MaxInput'])

        lColor = colorOps.multiplyColor(self['LeftColor'], 1+intensityL) 
        rColor = colorOps.multiplyColor(self['RightColor'], 1+intensityR) 

        lBound = l*scaleFactor
        rBound = screenWidth-(r*scaleFactor)
        
        ret = []
        ret.append({'Color': lColor, 'Location':'{x}<='+str(lBound)})
        ret.append({'Color': rColor, 'Location': '{x}>='+str(rBound)})

        return (ret, [{'Data': (l,r,intensityL, intensityR)}])
    def game3(self, sensors, recurses):
        if sensors:
            sets = eval(sensors[-1]['Data'])
        elif recurses:
            sets = recurses[-1]['Data']
            if len(sets) < 4:
                return ([],[])
        else:
            return ([], [])

        screenHeight = compReg.getComponent('Screen').getSize()[3]
        divisionSize = screenHeight / float(len(sets))
        ret  = []
        for i,(lineLocation,lIntense, rIntense) in enumerate(sets):
            if lineLocation == -1:
                continue
            baseSet = self.competition(lineLocation, lIntense, rIntense)[0] # disregarding recurses
            ylower = i*divisionSize
             
            for line in baseSet:
                line['Location'] += ', {y}>'+str(ylower-self['RowHeight']/2.)+','+\
                '{y}<'+str(ylower+self['RowHeight']/2.)
            ret += baseSet
        return (ret, [{'Data':sets}])

    def game4(self, sensors, recurses):
        if sensors:
            sets = eval(sensors[-1]['Data'])
        elif recurses:
            sets = recurses[-1]['Data']
            if len(sets) < 4:
                return ([],[])
        else:
            return ([], [])

        screenHeight = compReg.getComponent('Screen').getSize()[3]
        divisionSize = screenHeight / float(len(sets))
        ret  = []
        for i,(l,r,lIntense, rIntense) in enumerate(sets):
            baseSet = self.mix(l,r, lIntense, rIntense)[0] # disregarding recurses
            if l == -1:
                continue
            ylower = i*divisionSize
             
            for line in baseSet:
                line['Location'] += ', {y}>'+str(ylower-self['RowHeight']/2.)+','+\
                '{y}<'+str(ylower+self['RowHeight']/2.)
            ret += baseSet
        return (ret, [{'Data':sets}])
    def game5(self,sensors, recursives):
        (o,r) = self.game2(sensors, recursives)
        leftBound = compReg.getComponent('Screen').getSize()[2] / 2 - 3
        rightBound = compReg.getComponent('Screen').getSize()[2] / 2 + 3
        o.append({'Color':(255,255,255), 'Location':'{x}>'+str(leftBound) + \
                    ', {x}<'+str(rightBound)})
        return (o,r)
    def win(self):
        self['parentScope'].refreshInterval = 100
        if 'l' in self.mode:
            c = self['LeftColor']
        elif 'r' in self.mode:
            c = self['RightColor']
        elif 'b' in self.mode:
            c = colorOps.addColors(self['RightColor'], self['LeftColor'])
        return ([{'PixelEvent': RandomEvent({'Color':c}), 'Location':'True', 'Color':c}], [])
