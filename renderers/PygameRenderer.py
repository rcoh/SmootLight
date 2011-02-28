from operationscore.Renderer import *
import util.TimeOps as timeops 
import pygame
from pygame.locals import *
import pdb
import util.ComponentRegistry as compReg 
class PygameRenderer(Renderer):
    """PygameRenderer is a renderer which renders the LightSystem to a pygame display"""

    def initRenderer(self):
        pygame.init()
        if not 'Size' in self:
            size = (1000, 200) 
            print size
        else:
            size = self['Size']
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color(0,0,0))
        self.stopwatch = timeops.Stopwatch()
        self.stopwatch.start()
    
    def render(self, lightSystem, currentTime=timeops.time()):
        self.background.fill(Color(0,0,0))
        #print 'drawing color:',light.color
        if 'Scale' in self:
            scale = self['Scale']
        else:
            scale = 1
        for light in lightSystem:
            scaledLoc = [l*scale for l in light.location] 
            pygame.draw.circle(self.background, light.state(currentTime), scaledLoc, \
                scale)

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption(str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
