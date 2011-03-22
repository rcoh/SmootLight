from operationscore.PixelMapper import *
import math

class SimpleMapper(PixelMapper):
    """SimpleMapper is a PixelMapper which maps events to the nearest Pixel.  It also supports
    strings of the form:
    {x}>5, {y}<10, {x}*{y}<{x}, etc. (Conditions, separated by commas.  Standard python syntax such
    as and and or may also be
    used).  You may use 'math.' functions such as math.sqrt, etc.  It also accepts lists of strings"""
    def mappingFunction(self, eventLocation, screen):
        if type(eventLocation) == tuple:
            d, i = screen.tree.query(eventLocation, distance_upper_bound=self['CutoffDist'])
            if d < self['CutoffDist']: return [(i,1)]
            return []
        else:
            #{x}>5,{y}<k
            ret = []
            if not isinstance(eventLocation, list):
                eventLocation = eventLocation.replace('{x}', 'pixel.location[0]')
                eventLocation = eventLocation.replace('{y}', 'pixel.location[1]')
                conditions = eventLocation.split(',')
            else:
                conditions = eventLocation #TODO: check for lists of strings
            conditionLambdas = [eval('lambda pixel:'+condition) for condition in conditions]
            
            for i, pixel in enumerate(screen):
                try:
                    pixelValid = True
                    for p in conditionLambdas:
                        if p(pixel) == False:
                            pixelValid = False
                            continue
                    if pixelValid:
                        ret.append((i,1))
                except Exception as exp:
                    exp.message += 'Bad Event Condition'
                    raise exp
            return ret
