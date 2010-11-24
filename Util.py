import pdb
from xml.etree.ElementTree import ElementTree
import math,struct
#import json # json.loads() to decode string; json.dumps() to encode data
import socket
from pygame.locals import *
import time as clock
KINET_VERSION = 0x0001
KINET_MAGIC = 0x4adc0104
KINET_MOREMAGIC = 0xdeadbeef
KINET_DEEPMAGIC = 0xc001d00d
KINET_MAGICHASH = 0x69000420
KINET_PORTOUT = 0x0108
KINET_UNI = 0
CONFIG_PATH = 'config/'
kinetDict = {'flags': 0, 'startcode': 0, 'pad':0}
def dist(l1, l2):
    return math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def time():
    return clock.time()*1000
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
def combineColors(c1,c2):
    return [c1[i]+c2[i] for i in range(min(len(c1),len(c2)))]
def multiplyColor(color, percent):
    return tuple([channel*(percent) for channel in color])
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
    header.extend(struct.pack('L', KINET_MAGIC))
    header.extend(struct.pack('H', KINET_VERSION))
    header.extend(struct.pack('H', KINET_PORTOUT))
    header.extend(struct.pack('L', 0))
    return header
def kinetPortOut():
    header = kinetHeader()
    header.extend(struct.pack('L', KINET_UNI))
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


