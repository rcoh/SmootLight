#TODO: multithreaded-rendering
from operationscore.SmootCoreObject import *
class Renderer(SmootCoreObject):
    """Renderer abstract class.  Doesn't do much now, but might do more later.
    Inheriting classes MUST define render which takes a light system and renders it.
    Inheriting classes may define initRenderer which is called after the dictionary
    is pulled from config."""
    def init(self):
        self.initRenderer()
    def render(lightSystem):
        raise NotImplementedError
    def initRenderer(self):
        pass
