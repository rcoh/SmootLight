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
def setScreen(screen):
    globals()["screen"] = screen
def getScreen():
    return screen
def setComponentDict(componentDictRef):
    globals()["componentDict"] = componentDictRef
def getComponentById(cid):
    if cid in componentDict:
        return componentDict[cid]
    else:
        return None
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
#Given a dictionary of connections, returns their topological ordering -- (the
#order in which they can be visited such that all parents have been visited
#before their children.  Returns the order or None if no such ordering exists
#(the graph contains a cycle).
def topologicalSort(adjacencyDict):
    def dfsVisit(vertex):
        gray[vertex] = 1
        for child in adjacencyDict[vertex]:
            if not child in visited:
                if child in gray: #We have a cycle.  No topological ordering
                    #exists!
                    raise Exception('Cycle!') 
                dfsVisit(child)
        orderedList.insert(0, vertex)
        visited[vertex] = 1
    orderedList = []
    visited = {}
    gray = {}
    for vertex in adjacencyDict:
        try:
            if not vertex in visited:
                dfsVisit(vertex)
        except:
            return None #cycle
    return orderedList
def topoTest():
    adj = {'a':['d','c'], 'b':['c'], 'c':['e'], 'd':['e'], 'e':[]}
    print topologicalOrdering(adj)
def testXMLParse(fileName):
    #pdb.set_trace()
    config = ElementTree()
    config.parse(fileName)
    print generateArgDict(config.find('ChildElement'))
    print generateArgDict(config.find('Renderer'))
##CONSTANTS##
location = 'Location'


