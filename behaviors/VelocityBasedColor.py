from operationscore.Behavior import *
import colorsys
class VelocityBasedColor(Behavior):
    """VelocityBasedColor is a behavior which adds a color to a pixel response based on the value of
    its XVel field.  Specifically, it maps linearally from MinVel->MaxVel to MinHue->MaxHue."""

    def processResponse(self, sensors, recurses):
        ret = []
        for dataPacket in sensors:
            outDict = dict(dataPacket)
            if 'XVel' in dataPacket:
                outDict['Color'] = self.mappingFunc(dataPacket['XVel']) 
            ret.append(outDict)
        return (ret, [])
    def mappingFunc(self, velocity):
        mappedVelocity = (velocity - self['MinVel']) / self['MaxVel']
        if mappedVelocity > 1:
            mappedVelocity = 1

        hueValue = self['MinHue'] + mappedVelocity * (self['MaxHue']-self['MinHue'])
        sat = 1
        val = 1
        return [x*255 for x in colorsys.hsv_to_rgb(hueValue,sat,val)]
