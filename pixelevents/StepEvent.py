from operationscore.PixelEvent import *
from numpy import array

class StepEvent(PixelEvent):
    def initEvent(self):
        self.validateArgs('StepEvent.params')
        self.life = self["LightTime"]
    def state(self, time)
        if time==0: return [1,0,0], self.life
        else: return None
    @staticmethod
    def generate(onTime, color):
        args = {'LightTime': onTime, 'Color': color}
        return StepEvent(args)
