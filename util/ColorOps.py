import random
from util.TimeOps import Stopwatch
def randomColor():
    return [random.randint(0,255) for i in range(3)]
def chooseRandomColor(colorList):
    return random.choice(colorList)
def safeColor(c):
    return [min(channel,255) for channel in c]
def combineColors(c1,c2):
    return safeColor([c1[i]+c2[i] for i in range(min(len(c1),len(c2)))])
def multiplyColor(color, percent):
    return safeColor([fastMultiply(channel, percent, 1) for channel in color])

def fastMultiply(value, mult, acc):
    if type(mult) == type(int(5)):
        return value*mult
    return int(value)*int(mult*10**acc)*10**(-acc)

