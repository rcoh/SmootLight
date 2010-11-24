import time, Util
from operationscore.Input import *
import pygame
from pygame.locals import *
#This class processes input from an already running pygame instance and passes
#it to the parent.  This class requires an already running pygame instance.
class PygameInput(Input):
    def sensingLoop(self):
        #try:
            for event in pygame.event.get():
                if event.type is KEYDOWN:
                    self.respond({Util.location: (5,5),'Key': event.key})
                if event.type is MOUSEBUTTONDOWN:
                    self.respond({Util.location: pygame.mouse.get_pos()})
        #except:
            #raise Exception('Pygame not initialized.  Pygame must be \
            #initialized.')
