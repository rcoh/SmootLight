import random
import colorsys
from util.TimeOps import Stopwatch
def randomColor():
    return [random.randint(0,255) for i in range(3)]

def cycleColor(index, increments):
    return floatToIntColor(list(colorsys.hsv_to_rgb(index/float(increments), 0.75, 1)))

def chooseRandomColor(colorList):
    """Given a list of colors, pick one at random"""
    return random.choice(colorList)
def safeColor(c):
    """Ensures that a color is valid"""
    c[0] = c[0] if c[0] < 255 else 255
    c[1] = c[1] if c[1] < 255 else 255
    c[2] = c[2] if c[2] < 255 else 255
    return c

def combineColors(colors):
    result = [0,0,0]
    for c in colors:
        result[0] += c[0]
        result[1] += c[1]
        result[2] += c[2]
    return safeColor(result)

def multiplyColor(color, percent):
    return safeColor([channel*(percent) for channel in color])

def floatToIntColor(rgb):
    rgb[0] = int(rgb[0]*256 + .5)
    rgb[1] = int(rgb[1]*256 + .5)
    rgb[2] = int(rgb[2]*256 + .5)
    return safeColor(rgb)

def randomBrightColor():
    hue = random.random()
    sat = random.random()/2.0 + .5
    val = 1.0
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = [hue, sat, val]
    return floatToIntColor(ret)

def randomDimColor(value):
    hue = random.random()
    sat = random.random()/2.0 + .5
    val = value
    hue, sat, val = colorsys.hsv_to_rgb(hue, sat, val)
    ret = [hue, sat, val]
    return floatToIntColor(ret)

class Color(object):
    def __init__(self, r,g,b):
        self.rep = [r,g,b]
