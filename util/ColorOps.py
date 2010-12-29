import random
def randomColor():
    return [random.randint(0,255) for i in range(3)]
def chooseRandomColor(colorList):
    return random.choice(colorList)
def safeColor(c):
    return [min(channel,255) for channel in c]
def combineColors(c1,c2):
    return safeColor([c1[i]+c2[i] for i in range(min(len(c1),len(c2)))])
def fastMultiply(color, percent, acc=100):
    percent = int(percent*acc)
    color = colorToInt(color)
    color = [channel*percent for channel in color]

def colorToInt(color):
    return [int(channel) for channel in color]
def multiplyColor(color, percent):
    
    return safeColor([channel*(percent) for channel in color])
