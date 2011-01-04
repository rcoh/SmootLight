#import cProfile
import struct
import random
#from LightInstallation import main
numiter = 10000000
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
print('starting')
abc1()
print('starting')
abc2()
print('done')
#command = """abc1()"""
#cProfile.runctx(command, globals(), locals())

#command = """abc2()"""
#cProfile.runctx(command, globals(), locals())

