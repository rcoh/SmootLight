from operationscore.Renderer import *
import util.TimeOps as timeops 
import pygame
from pygame.locals import *
import pdb
class PygameRenderer(Renderer):
    """PygameRenderer is a renderer which renders the LightSystem to a pygame display"""

    def initRenderer(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1300,500))
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
                self['Scale'])

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption(str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
