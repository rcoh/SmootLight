#Geometry code
import math
from bisect import *
import random
def pointWithinBoundingBox(point, bb): 
    """Returns whether or not a point (x,y) is within a bounding box (xmin, ymin, xmax, ymax)"""
    return all([(point[i % 2] <= bb[i]) == (i>1) for i in range(4)])

def addLocations(l1,l2):
    return tuple([l1[i]+l2[i] for i in range(len(l1))])

def gaussian(x,height,center,width):
    a=height
    b=center
    c=width
    return a*math.exp(-((x-b)**2)/(2*c**2))

def dist(l1, l2):
    return math.sqrt((l1[0]-l2[0])**2+(l1[1]-l2[1])**2) #For speed

def randomLoc(maxBoundingBox, minBoundingBox=(0,0)): #TODO: make less shitty
    loc = []
    loc.append(random.randint(minBoundingBox[0], maxBoundingBox[0]))
    loc.append(random.randint(minBoundingBox[1], maxBoundingBox[1]))
    return tuple(loc)

def approxexp(x):
    """Approximates exp with a 3 term Taylor Series."""
    return 1+x+x**2/2+x**3/6

def windtrail(x,y,height,center,width):
    a=height
    b=center
    c=width
    return a*((math.exp(-((x-b))/(c)))**2)*(math.exp(-((y))/(0.2*c)))**2

class Location(object):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    def __add__(self, b):
        return Location(self.x+b.x, self.y+b.y)
