import time
import util.Strings as Strings
from operationscore.Input import *
import pygame
from pygame.locals import *
#This class processes input from an already running pygame instance and passes
#it to the parent.  This class requires an already running pygame instance.
class PygameInput(Input):
    """PygameInput is an input tied to the PygameDisplay.  Specify:
    <FollowMouse>True</FollowMouse> to receive an input every frame specifying the current mouse
    position.
    <Keyboard>True</Keyboard> to grab keystrokes
    <Clicks>True</Clicks> to grab clicks.

    NB: If follow mouse is enabled, PygameInput will not return mouse and keypresses.  You can, however,
    instantiate other PygameInputs in the XML that will capture mouse and keypresses."""
    def sensingLoop(self):
        if self['FollowMouse']:
            self.respond({Strings.LOCATION: pygame.mouse.get_pos()})
            return
        for event in pygame.event.get():
            if event.type is KEYDOWN:
                if event.key == 27:
                    self.die()
                if self['Keyboard']:
                    self.respond({'Key': event.key})
                    return
                else:
                    pygame.event.post(event)
            if event.type is MOUSEBUTTONDOWN:
                if self['Clicks']:
                    self.respond({Strings.LOCATION: pygame.mouse.get_pos()})
