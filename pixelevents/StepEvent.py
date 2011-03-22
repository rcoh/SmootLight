from operationscore.PixelEvent import *
from numpy import array

class StepEvent(PixelEvent):
    def initEvent(self):
        self.validateArgs('StepEvent.params')
        self.life = self["LightTime"] * 30
    def coeffs(self):
        self.life -= 1
        return array([0.,0.,0.]) if self.life==0 else array([1.,1.,0.])
    @staticmethod
    def generate(onTime, color):
        args = {'LightTime': onTime, 'Color': color}
        return StepEvent(args)

