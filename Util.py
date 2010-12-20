import pdb
from xml.etree.ElementTree import ElementTree
import math,struct
from bisect import *
#import json # json.loads() to decode string; json.dumps() to encode data
import socket
import random
from pygame.locals import *
from pixelevents.StepEvent import *

classArgsMem = {}
UNI = 0
colorByteMem = {}
CONFIG_PATH = 'config/'
kinetDict = {'flags': 0, 'startcode': 0, 'pad':0}
componentDict = {}
#Only for rough estimates.  Kindof lazy on specifics.
def pointWithinBoundingBox(point, bb): #this could be in 4 lines, but I'm lazy.
    return sum([(point[i % 2] <= bb[i]) == (i>1) for i in range(4)]) == 4 
print pointWithinBoundingBox((118,21), (10,8,298,42))
def addLocations(l1,l2):
    return tuple([l1[i]+l2[i] for i in range(len(l1))])
def addPixelEventIfMissing(responseDict):
    if not 'PixelEvent' in responseDict:
        if 'Color' in responseDict:
            color = responseDict['Color']
        else:
            raise Exception('Need Color.  Probably')
        responseDict['PixelEvent'] = StepEvent.generate(300, color)
def gaussian(x,height,center,width):
    a=height
    b=center
    c=width
    return a*math.exp(-((x-b)**2)/(2*c**2))
def dist(l1, l2):
    return math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def find_le(a, x):
    'Find rightmost value less than or equal to x'
    return bisect_right(a, x)-1

def find_ge(a, x):
    'Find leftmost value greater than x'
    return bisect_left(a, x)
def testXMLParse(fileName):
    #pdb.set_trace()
    config = ElementTree()
    config.parse(fileName)
    print generateArgDict(config.find('ChildElement'))
    print generateArgDict(config.find('Renderer'))
##CONSTANTS##
location = 'Location'


