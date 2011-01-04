#Geometry code
import math
from bisect import *
import random
def pointWithinBoundingBox(point, bb): #this could be in 4 lines, but I'm lazy.
    return sum([(point[i % 2] <= bb[i]) == (i>1) for i in range(4)]) == 4 
print pointWithinBoundingBox((118,21), (10,8,298,42))
def addLocations(l1,l2):
    return tuple([l1[i]+l2[i] for i in range(len(l1))])
def gaussian(x,height,center,width):
    a=height
    b=center
    c=width
    return a*math.exp(-((x-b)**2)/(2*c**2))
def dist(l1, l2):
    return math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def randomLoc(boundingBox): #TODO: make less shitty
    loc = []
    loc.append(random.randint(0, boundingBox[0]))
    loc.append(random.randint(0, boundingBox[1]))
    return tuple(loc)
