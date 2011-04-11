from numpy import zeros, concatenate
argDict = {'flags': 0, 'startcode': 0x0fff, 'pad':0}

# Allocate a buffer for transmitted packets and fill it with magic
xmit = zeros(174, dtype='ubyte')
xmit[:24] = bytearray('\x04\x01\xdcJ\x01\x00\x08\x01\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x96\x00\xff\x0f')

def composePixelStripPacket(pixelStrip, port, currentTime):
    xmit[16] = port
    xmit[24:] = concatenate([p.state(currentTime) for p in pixelStrip])
    return xmit
