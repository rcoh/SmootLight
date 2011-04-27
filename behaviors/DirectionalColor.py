from operationscore.Behavior import *
class DirectionalColor(Behavior):
    """DirectionalColor is a behavior which adds a color to pixel response
    based on the sign of its XVel field.
    Args:
        <PositiveColor>(X,X,X) -- the color to use if XVel > 0
        <NegativeColor>(X,X,X) -- the color to use if XVel < 0

    """
    def processResponse(self, sensors, recurses):
        ret = []
        for dataPacket in sensors:  
            outDict = dict(dataPacket)
            if 'XVel' in dataPacket:
                outDict['Color'] = self['PositiveColor'] if dataPacket['XVel'] > 0 else\
                    self['NegativeColor']
            ret.append(outDict)
        return (ret,[])
