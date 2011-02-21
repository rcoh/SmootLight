from operationscore.Input import *
from PIL import Image
import util.ComponentRegistry as compReg
import os
class JPGInput(Input):
    def inputInit(self):
        self.images = []
        self.imageIndex = 0
        compReg.getLock().acquire()
        minX,minY,maxX,maxY = compReg.getComponent('Screen').getSize()
        compReg.getLock().release()
        sWidth = maxX-minX
        sHeight = maxY-minY
        for filename in os.listdir(self['Directory']):
            path = os.path.join(self['Directory'], filename)
            if '.jpg' in path or '.bmp' in path:
                im = Image.open(path) #file to open
                (w,h)=im.size
                print w,h
                xScale = sWidth/float(w)
                yScale = sHeight/float(h)
                pixels = []
                for x in range(0,w,5):
                   for y in range(0,h,5):
                       rgb = im.getpixel((x,y))
                       pixels.append({'Location':(int(x*xScale+minX),int(minY+y*yScale)),'Color':rgb})
                self.images.append(pixels)

    def sensingLoop(self):
        self.imageIndex += 1
        self.imageIndex = self.imageIndex % len(self.images)
        self.respond(self.images[self.imageIndex])
