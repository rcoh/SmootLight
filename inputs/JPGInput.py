from operationscore.Input import *
from PIL import Image
import os
class JPGInput(Input):
    def inputInit(self):
        self.images = []
        self.imageIndex = 0
        files = os.listdir(self['Directory'])
        files.sort()
        for filename in files:
            print filename
            path = os.path.join(self['Directory'], filename)
            if '.jpg' in path or '.bmp' in path:
                im = Image.open(path) #file to open
                self.images.append(im)

    def sensingLoop(self):
        self.imageIndex += 1
        self.imageIndex = self.imageIndex % len(self.images)
        self.respond(dict(Image=self.images[self.imageIndex]))
