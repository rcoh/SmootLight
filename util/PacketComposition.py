import struct
VERSION = 0x0001
MAGIC = 0x4adc0104
MOREMAGIC = 0xdeadbeef
DEEPMAGIC = 0xc001d00d
MAGICHASH = 0x69000420
PORTOUT = 0x0108
UNI = 0
import pdb
kinetDict = {'flags': 0, 'startcode': 0, 'pad':0}
def composePixelStripData(pixelStrip):
    packet = bytearray()
    for light in pixelStrip:
        color = light.state()
        for channel in color: #skip the last value, its an
            #alpha value
            packet.append(struct.pack('B', channel))
    return packet
#    packet = [0]*len(pixelStrip.pixels)*3 #preallocate for speed
#    for i in range(len(pixelStrip.pixels)): 
#color = pixelStrip.pixels[i].state()
#packet[i:i+2] = color
#    return bytearray(packet)
def composePixelStripPacket(pixelStrip,port):
    packet = bytearray()
    data = composePixelStripData(pixelStrip)
    subDict = dict(kinetDict)
    subDict['len'] = 38000 #I have no idea why this works.
    subDict['port'] = port
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
    payload.extend(struct.pack('H', argDict['flags']))
    #payload.append(0x00) #somepadding? lolwtf.
    payload.extend(struct.pack('H', argDict['len']))
    payload.extend(struct.pack('H', argDict['startcode']))
    return payload
def kinetPortOutPacket(payloadArgs):
    packet = bytearray()
    packet.extend(kinetPortOut())
    packet.extend(kinetPortOutPayload(payloadArgs))
    return packet
