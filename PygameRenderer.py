from Renderer import Renderer
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
    def render(self, lightSystem):
        self.background.fill(Color('Black'))
        #print 'drawing color:',light.color
        for light in lightSystem:
            pygame.draw.circle(self.background, light.lightState(), light.location, \
                light.radius)

        self.screen.blit(self.background, (0,0))
        pygame.display.flip()
