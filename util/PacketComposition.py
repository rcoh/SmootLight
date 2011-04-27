from numpy import zeros
argDict = {'flags': 0, 'startcode': 0x0fff, 'pad':0}

# Allocate a buffer for transmitted packets and fill it with magic
# Only works for strips of 50 pixels
xmit = zeros(174, dtype='ubyte')
xmit[:8], xmit[20:24] = [4,1,220,74,1,0,8,1], [150,0,255,15]

def composePixelStripPacket(values, port):
    xmit[16], xmit[24:] = port, values.ravel()
    return xmit
