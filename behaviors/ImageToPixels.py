from operationscore.Behavior import *
import util.ComponentRegistry as compReg
from PIL import Image
class ImageToPixels(Behavior):
    def processResponse(self, sensors, recurs):
        ret = []
        if sensors and 'Image' in sensors[0]:
            dataPacket = sensors[0]
            screen = compReg.getComponent('Screen')
            im = dataPacket['Image'] 
            minX,minY,maxX,maxY = compReg.getComponent('Screen').size
            sWidth = maxX-minX
            sHeight = maxY-minY
            (imageWidth,imageHeight)=im.size
            for light in screen:
                lightLoc = light.location
                imageLoc = ((lightLoc[0]-minX)*(imageWidth-1) / sWidth, (lightLoc[1]-minY)*\
                            (imageHeight-1)/sHeight)
                try:
                    pixelColor = im.getpixel(imageLoc)
                except:
                    pdb.set_trace()
                    print lightLoc
                ret.append(dict(Location=lightLoc, Color=pixelColor))
        return (ret, [])
