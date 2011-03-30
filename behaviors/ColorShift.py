import util.ColorOps as colorOps
from operationscore.Behavior import *
import colorsys
class ColorShift(Behavior):
    def processResponse(self, sensor, recurs):
        ret = []
        for data in sensor:
<<<<<<< HEAD
            if not 'HSV' in data:
		colors = [d/255.0 for d in data['Color']]
                data['HSV'] = list(colorsys.rgb_to_hsv(*colors))
	    if not self['Increment']:
		self['Increment'] = 0.005
=======
            #if not 'HSV' in data:
            colors = [d/255.0 for d in data['Color']]
            data['HSV'] = list(colorsys.rgb_to_hsv(*colors))
            if not self['Increment']:
                self['Increment'] = 0.005
>>>>>>> b473b5443e2e5403e7ce0af932c7ed60855bf2e4
            data['HSV'][0] += self['Increment']
            if data['HSV'][0] >= 1:
                data['HSV'][0] = 0
            colors = colorsys.hsv_to_rgb(*data['HSV'])
            data['Color'] = [d*255.0 for d in colors]
            ret.append(data)
        return (ret,[])
