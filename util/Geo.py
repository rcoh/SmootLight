#Geometry code
import math
from bisect import *
import random
def pointWithinBoundingBox(point, bb): #this could be in 4 lines, but I'm lazy.
    return sum([(point[i % 2] <= bb[i]) == (i>1) for i in range(4)]) == 4 

def addLocations(l1,l2):
    return tuple([l1[i]+l2[i] for i in range(len(l1))])

def gaussian(x,height,center,width):
    a=height
    b=center
    c=width
    return a*math.exp(-((x-b)**2)/(2*c**2))

def dist(l1, l2):
    return math.sqrt((l1[0]-l2[0])**2+(l1[1]-l2[1])**2) #For speed

def randomLoc(boundingBox): #TODO: make less shitty
    loc = []
    loc.append(random.randint(0, boundingBox[0]))
    loc.append(random.randint(0, boundingBox[1]))
    return tuple(loc)

def approxexp(x):
    """Approximates exp with a 3 term Taylor Series."""
    return 1+x+x**2/2+x**3/6

def windtrail(x,y,height,center,width):
    a=height
    b=center
    c=width
    return a*((math.exp(-((x-b))/(c)))**2)*(math.exp(-((y))/(0.2*c)))**2
