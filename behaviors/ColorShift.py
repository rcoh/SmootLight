import util.ColorOps as colorOps
from operationscore.Behavior import *
import colorsys
class ColorShift(Behavior):
    def processResponse(self, sensor, recurs):
        ret = []
        for data in sensor:
            if not 'HSV' in data:
                data['HSV'] = list(colorsys.rgb_to_hsv(*data['Color']))
            
            data['HSV'][0] += .01
            if data['HSV'][0] >= 360:
                data['HSV'][0] = 0
            data['Color'] = colorsys.hsv_to_rgb(*data['HSV'])
            ret.append(data)
        return (ret,[])
