from operationscore.Renderer import *
import util.TimeOps as timeops 
import pygame
from pygame.locals import *
import pdb
class PygameRenderer(Renderer):
    def initRenderer(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1300,50))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(Color('Black'))
        self.stopwatch = timeops.Stopwatch()
        self.stopwatch.start()
    def render(self, lightSystem, currentTime=timeops.time()):
        self.background.fill(Color('Black'))
        #print 'drawing color:',light.color
        for light in lightSystem:
            pygame.draw.circle(self.background, light.state(currentTime), light.location, \
                light.radius)

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.stopwatch.stop()
        pygame.display.set_caption(str(int(1000/self.stopwatch.elapsed())))
        self.stopwatch.start()
