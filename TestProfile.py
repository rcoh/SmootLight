import cProfile
import struct
import random
import math
#from LightInstallation import main
numiter = 1000000
def main1():
    for i in xrange(0,numiter):
        if 'abc' == 'def':
            pass
        if 'abc' == 'abc':
            pass

def main2():
    for i in xrange(0,numiter):
        if 1 == 2:
            pass
        if 1 == 1:
            pass

x = [1,2,3]
a = []
def abc1():
    for i in range(0,numiter):
        a = min(4, 255)
        b = min(257, 255)

def abc2():
    for i in range(0,numiter):
        a = 4 if 4 < 255 else 255
        b = 257 if 257 < 255 else 255
def strucpack():
    for i in xrange(0,numiter):
        b = struct.pack('B', random.randint(0,255))
def dictlookup():
    lookup = {}
    for i in xrange(0,256):
        lookup[i] = struct.pack('B', random.randint(0,255))
    for i in xrange(0,numiter):
        b = lookup[random.randint(0,255)]
def dist1():
    l1 = [21.43, 5423.123]
    l2 = [123, 12312345]
    for i in xrange(0,numiter):
        d = math.sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))
def dist2():
    l1 = [21.43, 5423.123]
    l2 = [123, 12312345]
    for i in xrange(0,numiter):
        d = math.sqrt((l1[0]-l2[0])**2+(l1[1]-l2[1])**2)
def exptest():
    for i in xrange(0, numiter):
        a = math.exp(-1)
    print a
def expapprox():
    for i in xrange(0, numiter):
        a = 1+-1+(-1)**2/float(2)
    print a
command = """exptest()"""
cProfile.runctx(command, globals(), locals())

command = """expapprox()"""
cProfile.runctx(command, globals(), locals())

