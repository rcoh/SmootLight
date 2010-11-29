import pdb
from xml.etree.ElementTree import ElementTree
import math,struct
#import json # json.loads() to decode string; json.dumps() to encode data
import socket
import random
from pygame.locals import *
import time as clock
from pixelevents.StepEvent import *
VERSION = 0x0001
MAGIC = 0x4adc0104
MOREMAGIC = 0xdeadbeef
DEEPMAGIC = 0xc001d00d
MAGICHASH = 0x69000420
PORTOUT = 0x0108
UNI = 0
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
def dist(l1, l2):
    return math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def time():
    return clock.time()*1000
def randomColor():
    return [random.randint(0,255) for i in range(3)]
def loadParamRequirementDict(className):
    return fileToDict(CONFIG_PATH + className)
def loadConfigFile(fileName):
    fileName = CONFIG_PATH + fileName
    if '.params' in fileName:
        return fileToDict(fileName)
    if '.xml' in fileName:
        config = ElementTree()
        config.parse(fileName)
        return config
def fileToDict(fileName):
    fileText = ''
    with open(fileName) as f:
        for line in f:
            fileText += line.rstrip('\n').lstrip('\t') + ' ' 
    if fileText == '':
        return {}
    return eval(fileText)
def safeColor(c):
    return [min(channel,255) for channel in c]
def combineColors(c1,c2):
    return safeColor([c1[i]+c2[i] for i in range(min(len(c1),len(c2)))])
def multiplyColor(color, percent):
    return safeColor(tuple([channel*(percent) for channel in color]))
#parses arguments into python objects if possible, otherwise leaves as strings
def generateArgDict(parentNode, recurse=False):
    args = {}
    for arg in parentNode.getchildren():
        key = arg.tag
        if arg.getchildren() != []:
            value = generateArgDict(arg, True)
        else:
            #convert into python if possible, otherwise don't
            try:
                value = eval(arg.text)
            except (NameError,SyntaxError):
                value = str(arg.text)
        if key in args: #build of lists of like-elements
            if type(args[key]) != type([]):
                args[key] = [args[key]]
            args[key].append(value)
        else:
            args[key]=value
    #if we should be a list but we aren't:
    if len(args.keys()) == 1 and recurse:
        return args[args.keys()[0]]
    return args
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
def getConnectedSocket(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print (ip, port)
    sock.connect((ip, port))
    return sock
def composePixelStripData(pixelStrip):
    packet = bytearray()
    for light in pixelStrip:
        color = light.state()
        for channel in color: #skip the last value, its an
            #alpha value
            packet.append(struct.pack('B', channel))
    #pdb.set_trace()
    return packet
def composePixelStripPacket(pixelStrip,port):
    packet = bytearray()
    data = composePixelStripData(pixelStrip)
    subDict = dict(kinetDict)
    subDict['len'] = 38399 #I have no idea why this works.
    subDict['port'] = port
    #pdb.set_trace()
    packet.extend(kinetPortOutPacket(subDict))
    packet.append(0x0)
    packet.extend(data)
    return packet
def kinetHeader():
    header = bytearray()
    header.extend(struct.pack('L', MAGIC))
    header.extend(struct.pack('H', VERSION))
    header.extend(struct.pack('H', PORTOUT))
    header.extend(struct.pack('L', 0))
    return header
def kinetPortOut():
    header = kinetHeader()
    header.extend(struct.pack('L', UNI))
    return header
def kinetPortOutPayload(argDict):
    payload = bytearray()
    payload.extend(struct.pack('B', argDict['port']))
    #payload.append(0x00) #somepadding? lolwtf.
    payload.extend(struct.pack('H', argDict['flags']))
    #payload.append(0x00) #somepadding? lolwtf.
    payload.extend(struct.pack('H', argDict['len']))
    payload.extend(struct.pack('H', argDict['startcode']))
    #pdb.set_trace()
    return payload
def kinetPortOutPacket(payloadArgs):
    packet = bytearray()
    packet.extend(kinetPortOut())
    packet.extend(kinetPortOutPayload(payloadArgs))
    return packet
def testXMLParse(fileName):
    #pdb.set_trace()
    config = ElementTree()
    config.parse(fileName)
    print generateArgDict(config.find('ChildElement'))
    print generateArgDict(config.find('Renderer'))

##CONSTANTS##
location = 'Location'


