from operationscore.Behavior import *
import util.ComponentRegistry as compReg
import util.BehaviorQuerySystem as bqs
import util.Geo as Geo
class GrowNear(Behavior):
    """GrowNear is a behavior designed to be used as a recursive hook to ResponseMover to move pixels by
    XStep.  As XStep are maintained in the responses itself, they can be
    modulated to facilitate, acceleration, modulation, bouncing, etc.  Specify:
    <XStep> -- the starting XStep
    """

    def processResponse(self, sensor, recurs):
        ret = []

        if self['GrowthDirection'] != None:
            growthDirection = self['GrowthDirection']
        else:
            growthDirection = 'right'
        if self['HitSensitivity'] != None:
            hitSensitivity = self['HitSensitivity']
        else:
            hitSensitivity = 4
        if self['MaxVelocity'] != None:
            maxVelocity = self['MaxVelocity']
        else:
            maxVelocity = 10
        if self['MinVelocity'] != None:
            minVelocity = self['MinVelocity']
        else:
            minVelocity = -1
        if self['MinLength'] != None:
            minLength = self['MinLength']
        else:
            minLength = 30

        for sensory in sensor:
            opsensory = dict(sensory)

            if not 'XVel' in opsensory:
                opsensory['XVel'] = -1
            if not 'SpeedupTimer' in opsensory:
                opsensory['SpeedupTimer'] = 0
 
            if growthDirection == 'right':
                results = bqs.query([
                    bqs.getBehaviorIdLambda('accelerate'),\
                    bqs.getDirectionLambda('-'),\
                    bqs.getLeftLambda(0)
                ])
            else:
                compReg.getLock().acquire()
                self.minX, self.minY, self.maxX, self.maxY = compReg.getComponent('Screen').size
                compReg.getLock().release()

                results = bqs.query([
                    bqs.getBehaviorIdLambda('accelerate'),\
                    bqs.getDirectionLambda('+'),\
                    bqs.getRightLambda(self.maxX)
                ])


            if results:
                opsensory['SpeedupTimer'] = hitSensitivity 

            if opsensory['SpeedupTimer'] > 0:
                opsensory['XVel'] = min(opsensory['XVel'] + 1, maxVelocity)
                opsensory['SpeedupTimer'] = opsensory['SpeedupTimer'] - 1
            else:
                opsensory['XVel'] = max(minVelocity, opsensory['XVel'] - 1)

            opsensory['Location'] = (opsensory['Location'][0], opsensory['Location'][1] + opsensory['XVel'])

            #Set min length
            if opsensory['Location'][1] <= minLength:
                opsensory['Location'] = (opsensory['Location'][0], minLength)
            print opsensory['Location']

            ret.append(opsensory)
        return (ret, []) 

