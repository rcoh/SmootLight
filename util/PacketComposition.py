import struct
VERSION = 0x0001
MAGIC = 0x4adc0104
PORTOUT = 0x0108
UNI = 0
import pdb
import util.TimeOps as timeops
argDict = {'flags': 0, 'startcode': 0x0fff, 'pad':0}

def composePixelStripData(pixelStrip,currentTime=timeops.time()):
    packet = bytearray()
    for value in pixelStrip.ravel():
        packet.append(struct.pack('B', value))
    return packet
#    packet = [0]*len(pixelStrip.pixels)*3 #preallocate for speed
#    for i in range(len(pixelStrip.pixels)): 
#color = pixelStrip.pixels[i].state()
#packet[i:i+2] = color
#    return bytearray(packet)

cache = {}
def memoize(f):
    def helper(x):
        if x not in cache:            
            cache[x] = f(x)
        return cache[x]
    return helper

@memoize
def cachePacketHeader(port):
    packet = bytearray()
    subDict = dict(argDict)
    subDict['len'] = 150 #I have no idea why this works.
    subDict['port'] = port
    packet.extend(portOutPacket(subDict))
#    packet.append(0x0)
    return packet

def composePixelStripPacket(pixelStrip,port, currentTime):
    packet = bytearray(cachePacketHeader(port))
    data = composePixelStripData(pixelStrip, currentTime)
    packet.extend(data)
    return packet

def packheader():
    header = bytearray()
    header.extend(struct.pack('L', MAGIC))
    header.extend(struct.pack('H', VERSION))
    header.extend(struct.pack('H', PORTOUT))
    header.extend(struct.pack('L', 0))
    return header

def portOut():
    header = packheader()
    header.extend(struct.pack('L', UNI))
    return header

def portOutPayload(argDict):
    payload = bytearray()
    payload.extend(struct.pack('B', argDict['port']))
    payload.extend(struct.pack('B',0))
    payload.extend(struct.pack('H', argDict['flags']))
    payload.extend(struct.pack('H', argDict['len']))
    payload.extend(struct.pack('H', argDict['startcode']))
    return payload
def composeSynchPacket():
    header = bytearray()
    header.extend(struct.pack('L', MAGIC))
    header.extend(struct.pack('H', VERSION))
    header.extend(struct.pack('H', 0x0109))
    header.extend(struct.pack('L', 0))
    header.extend(struct.pack('L', 0))
    return header

def portOutPacket(payloadArgs):
    packet = bytearray()
    packet.extend(portOut())
    packet.extend(portOutPayload(payloadArgs))
    return packet
