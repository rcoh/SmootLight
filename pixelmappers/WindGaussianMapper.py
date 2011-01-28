from operationscore.PixelMapper import *
import util.Geo as Geo
import math
class WindGaussianMapper(PixelMapper):
    def mappingFunction(self, eventLocation, screen):
        returnPixels = [] #TODO: consider preallocation and trimming
        [x,y] = eventLocation
        potentialPixels = screen.pixelsInRange(x-self.CutoffDist, x)
        for (xloc,pixel) in screen.pixelsInRange(x-self.CutoffDist, x):
            pixelDistx = math.fabs(pixel.location[0] - x)
            pixelDisty = math.fabs(pixel.location[1] - y)
            if pixelDistx < self.CutoffDist:
		if pixelDisty < 30:
	                w = Geo.windtrail(pixelDistx, pixelDisty, self.Height, 0, self.Width)
	                if w > self.MinWeight:
        	            returnPixels.append((pixel, w))

        return returnPixels
