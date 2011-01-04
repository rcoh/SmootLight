import random
def randomColor():
    return [random.randint(0,255) for i in range(3)]
def chooseRandomColor(colorList):
    return random.choice(colorList)
def safeColor(c):
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
